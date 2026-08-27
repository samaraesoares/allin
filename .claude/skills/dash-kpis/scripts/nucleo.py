#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Núcleo do painel: banco, regras e cálculos.

Zero dependência externa: só Python 3 e SQLite, que já vêm no computador.
O banco fica em financeiro/dash.db, na raiz do seu workspace.
"""

import os
import sqlite3
from datetime import date, datetime

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
BANCO = os.environ.get("DASH_DB") or os.path.join(RAIZ, "financeiro", "dash.db")

ESTAGIOS = ["novo", "conversa", "proposta", "negociacao", "fechado", "perdido"]
TIPOS_EVENTO = ["contato", "reuniao", "proposta_enviada", "fechado", "perdido"]

SCHEMA = """
CREATE TABLE IF NOT EXISTS config (
  chave TEXT PRIMARY KEY,
  valor TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS clientes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT NOT NULL UNIQUE,
  valor REAL NOT NULL DEFAULT 0,
  tipo TEXT NOT NULL DEFAULT 'recorrente' CHECK (tipo IN ('recorrente','projeto')),
  status TEXT NOT NULL DEFAULT 'ativo' CHECK (status IN ('ativo','pausado','ex')),
  entrada TEXT NOT NULL DEFAULT (date('now','localtime')),
  saida TEXT,
  motivo_saida TEXT,
  nota TEXT
);

CREATE TABLE IF NOT EXISTS recebimentos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cliente_id INTEGER REFERENCES clientes(id),
  cliente TEXT NOT NULL,
  valor REAL NOT NULL,
  data TEXT NOT NULL DEFAULT (date('now','localtime')),
  descricao TEXT
);

CREATE TABLE IF NOT EXISTS leads (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT NOT NULL,
  empresa TEXT,
  origem TEXT NOT NULL DEFAULT 'outro',
  ticket REAL DEFAULT 0,
  estagio TEXT NOT NULL DEFAULT 'novo',
  criado_em TEXT NOT NULL DEFAULT (date('now','localtime')),
  atualizado_em TEXT NOT NULL DEFAULT (date('now','localtime')),
  nota TEXT
);

CREATE TABLE IF NOT EXISTS eventos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  lead_id INTEGER REFERENCES leads(id),
  tipo TEXT NOT NULL,
  data TEXT NOT NULL DEFAULT (date('now','localtime')),
  valor REAL,
  nota TEXT
);

CREATE TABLE IF NOT EXISTS fechamentos (
  mes TEXT PRIMARY KEY,
  faturado REAL NOT NULL DEFAULT 0,
  recorrente REAL NOT NULL DEFAULT 0,
  clientes_ativos INTEGER NOT NULL DEFAULT 0,
  entradas INTEGER NOT NULL DEFAULT 0,
  saidas INTEGER NOT NULL DEFAULT 0,
  fechado_em TEXT NOT NULL DEFAULT (date('now','localtime'))
);
"""

PADRAO_CONFIG = {
    "negocio": "Meu negócio",
    "moeda": "R$",
    "meta_recorrente": "0",
    "meta_faturamento_mes": "0",
    "custo_fixo_mes": "0",
}


# ---------------------------------------------------------------- banco

def conectar():
    """Abre o banco, criando o arquivo e o schema na primeira vez."""
    os.makedirs(os.path.dirname(BANCO), exist_ok=True)
    con = sqlite3.connect(BANCO)
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    for chave, valor in PADRAO_CONFIG.items():
        con.execute("INSERT OR IGNORE INTO config (chave, valor) VALUES (?,?)", (chave, valor))
    con.commit()
    return con


def config(con):
    return {linha["chave"]: linha["valor"] for linha in con.execute("SELECT * FROM config")}


def definir_config(con, chave, valor):
    con.execute(
        "INSERT INTO config (chave, valor) VALUES (?,?) "
        "ON CONFLICT(chave) DO UPDATE SET valor=excluded.valor",
        (chave, str(valor)),
    )
    con.commit()


def numero(valor, padrao=0.0):
    try:
        return float(str(valor).replace(".", "").replace(",", ".")) if isinstance(valor, str) else float(valor)
    except (TypeError, ValueError):
        return padrao


def mes_de(texto=None):
    """AAAA-MM do texto (AAAA-MM-DD ou AAAA-MM) ou do mês corrente."""
    if not texto:
        return date.today().strftime("%Y-%m")
    return str(texto)[:7]


# ---------------------------------------------------------------- clientes

def add_cliente(con, nome, valor=0, tipo="recorrente", entrada=None, nota=None):
    con.execute(
        "INSERT INTO clientes (nome, valor, tipo, entrada, nota) VALUES (?,?,?,?,?) "
        "ON CONFLICT(nome) DO UPDATE SET valor=excluded.valor, tipo=excluded.tipo, status='ativo', saida=NULL",
        (nome, numero(valor), tipo, entrada or date.today().isoformat(), nota),
    )
    con.commit()
    return con.execute("SELECT * FROM clientes WHERE nome=?", (nome,)).fetchone()


def churn(con, nome, motivo=None, data=None):
    cur = con.execute(
        "UPDATE clientes SET status='ex', saida=?, motivo_saida=? WHERE nome=?",
        (data or date.today().isoformat(), motivo, nome),
    )
    con.commit()
    return cur.rowcount


def receber(con, cliente, valor, data=None, descricao=None):
    linha = con.execute("SELECT id FROM clientes WHERE nome=?", (cliente,)).fetchone()
    con.execute(
        "INSERT INTO recebimentos (cliente_id, cliente, valor, data, descricao) VALUES (?,?,?,?,?)",
        (linha["id"] if linha else None, cliente, numero(valor), data or date.today().isoformat(), descricao),
    )
    con.commit()


# ---------------------------------------------------------------- funil

def add_lead(con, nome, empresa=None, ticket=0, origem="outro", nota=None):
    cur = con.execute(
        "INSERT INTO leads (nome, empresa, ticket, origem, nota) VALUES (?,?,?,?,?)",
        (nome, empresa, numero(ticket), origem, nota),
    )
    con.commit()
    return cur.lastrowid


def achar_lead(con, nome):
    return con.execute(
        "SELECT * FROM leads WHERE nome LIKE ? OR empresa LIKE ? ORDER BY atualizado_em DESC LIMIT 1",
        ("%" + nome + "%", "%" + nome + "%"),
    ).fetchone()


def mover_lead(con, nome, estagio, valor=None, nota=None):
    """Move o lead de estágio. 'fechado' com valor cria o cliente na hora."""
    if estagio not in ESTAGIOS:
        raise ValueError("estágio inválido: %s (use um de: %s)" % (estagio, ", ".join(ESTAGIOS)))
    lead = achar_lead(con, nome)
    if not lead:
        raise ValueError("não achei lead com esse nome: %s" % nome)
    con.execute(
        "UPDATE leads SET estagio=?, atualizado_em=? WHERE id=?",
        (estagio, date.today().isoformat(), lead["id"]),
    )
    tipo = {"proposta": "proposta_enviada", "fechado": "fechado", "perdido": "perdido"}.get(estagio, "contato")
    con.execute(
        "INSERT INTO eventos (lead_id, tipo, valor, nota) VALUES (?,?,?,?)",
        (lead["id"], tipo, numero(valor) if valor is not None else lead["ticket"], nota),
    )
    con.commit()
    if estagio == "fechado":
        add_cliente(con, lead["nome"], numero(valor) if valor is not None else lead["ticket"])
    return lead


# ---------------------------------------------------------------- leitura

def resumo(con, mes=None):
    cfg = config(con)
    mes = mes_de(mes)
    moeda = cfg.get("moeda", "R$")

    ativos = con.execute("SELECT * FROM clientes WHERE status='ativo' ORDER BY valor DESC").fetchall()
    recorrente = sum(c["valor"] for c in ativos if c["tipo"] == "recorrente")

    faturado = con.execute(
        "SELECT COALESCE(SUM(valor),0) t FROM recebimentos WHERE substr(data,1,7)=?", (mes,)
    ).fetchone()["t"]

    entradas = con.execute(
        "SELECT COUNT(*) n FROM clientes WHERE substr(entrada,1,7)=?", (mes,)
    ).fetchone()["n"]
    saidas = con.execute(
        "SELECT COUNT(*) n FROM clientes WHERE saida IS NOT NULL AND substr(saida,1,7)=?", (mes,)
    ).fetchone()["n"]

    funil = []
    for estagio in ESTAGIOS[:4]:
        linha = con.execute(
            "SELECT COUNT(*) n, COALESCE(SUM(ticket),0) t FROM leads WHERE estagio=?", (estagio,)
        ).fetchone()
        funil.append({"estagio": estagio, "quantidade": linha["n"], "valor": linha["t"]})

    pipeline = con.execute(
        "SELECT COALESCE(SUM(ticket),0) t FROM leads WHERE estagio IN ('conversa','proposta','negociacao')"
    ).fetchone()["t"]

    propostas_mes = con.execute(
        "SELECT COUNT(*) n FROM eventos WHERE tipo='proposta_enviada' AND substr(data,1,7)=?", (mes,)
    ).fetchone()["n"]
    fechados_mes = con.execute(
        "SELECT COUNT(*) n FROM eventos WHERE tipo='fechado' AND substr(data,1,7)=?", (mes,)
    ).fetchone()["n"]

    meta_rec = numero(cfg.get("meta_recorrente", 0))
    custo = numero(cfg.get("custo_fixo_mes", 0))

    return {
        "negocio": cfg.get("negocio", "Meu negócio"),
        "moeda": moeda,
        "mes": mes,
        "recorrente": recorrente,
        "meta_recorrente": meta_rec,
        "falta_meta": max(0.0, meta_rec - recorrente),
        "percentual_meta": round(recorrente / meta_rec * 100, 1) if meta_rec else None,
        "faturado_mes": faturado,
        "meta_faturamento_mes": numero(cfg.get("meta_faturamento_mes", 0)),
        "custo_fixo_mes": custo,
        "sobra": recorrente - custo,
        "clientes_ativos": len(ativos),
        "entradas_mes": entradas,
        "saidas_mes": saidas,
        "ticket_medio": round(recorrente / len([c for c in ativos if c["tipo"] == "recorrente"]), 2)
        if any(c["tipo"] == "recorrente" for c in ativos) else 0,
        "pipeline": pipeline,
        "propostas_mes": propostas_mes,
        "fechados_mes": fechados_mes,
        "taxa_fechamento": round(fechados_mes / propostas_mes * 100, 1) if propostas_mes else None,
        "carteira": [dict(c) for c in ativos],
        "funil": funil,
        "leads": [dict(l) for l in con.execute(
            "SELECT * FROM leads WHERE estagio NOT IN ('fechado','perdido') ORDER BY ticket DESC LIMIT 20"
        )],
        "historico": [dict(f) for f in con.execute(
            "SELECT * FROM fechamentos ORDER BY mes DESC LIMIT 12"
        )],
        "concentracao": round(max([c["valor"] for c in ativos] or [0]) / recorrente * 100, 1) if recorrente else 0,
    }


def fechar_mes(con, mes=None):
    """Grava a fotografia do mês. Rode no último dia útil."""
    mes = mes_de(mes)
    r = resumo(con, mes)
    con.execute(
        "INSERT INTO fechamentos (mes, faturado, recorrente, clientes_ativos, entradas, saidas, fechado_em) "
        "VALUES (?,?,?,?,?,?,?) ON CONFLICT(mes) DO UPDATE SET "
        "faturado=excluded.faturado, recorrente=excluded.recorrente, clientes_ativos=excluded.clientes_ativos, "
        "entradas=excluded.entradas, saidas=excluded.saidas, fechado_em=excluded.fechado_em",
        (mes, r["faturado_mes"], r["recorrente"], r["clientes_ativos"], r["entradas_mes"], r["saidas_mes"],
         datetime.now().strftime("%Y-%m-%d")),
    )
    con.commit()
    return r


def dinheiro(valor, moeda="R$"):
    """Formata no padrão brasileiro: R$ 3.200,00 (inclusive negativo)."""
    bruto = "{:,.2f}".format(float(valor or 0))          # 3,200.00
    return "%s %s" % (moeda, bruto.replace(",", "X").replace(".", ",").replace("X", "."))


def resumo_texto(r):
    """Resumo em markdown, pro Claude colar na conversa ou no fechamento do mês."""
    m = r["moeda"]
    linhas = [
        "## Painel — %s (%s)" % (r["negocio"], r["mes"]),
        "",
        "| Indicador | Valor |",
        "|---|---|",
        "| Recorrente | %s |" % dinheiro(r["recorrente"], m),
        "| Meta de recorrente | %s%s |" % (
            dinheiro(r["meta_recorrente"], m),
            (" (%s%%)" % r["percentual_meta"]) if r["percentual_meta"] is not None else "",
        ),
        "| Faturado no mês | %s |" % dinheiro(r["faturado_mes"], m),
        "| Custo fixo | %s |" % dinheiro(r["custo_fixo_mes"], m),
        "| Sobra sobre o fixo | %s |" % dinheiro(r["sobra"], m),
        "| Clientes ativos | %s (entraram %s, saíram %s) |" % (r["clientes_ativos"], r["entradas_mes"], r["saidas_mes"]),
        "| Ticket médio | %s |" % dinheiro(r["ticket_medio"], m),
        "| Pipeline aberto | %s |" % dinheiro(r["pipeline"], m),
        "| Propostas no mês | %s |" % r["propostas_mes"],
        "| Fechamentos no mês | %s%s |" % (
            r["fechados_mes"],
            (" (%s%% das propostas)" % r["taxa_fechamento"]) if r["taxa_fechamento"] is not None else "",
        ),
        "| Maior cliente | %s%% do recorrente |" % r["concentracao"],
    ]
    return "\n".join(linhas)
