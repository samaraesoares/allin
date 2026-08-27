#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Agenda e tarefas em cima de tarefas.md. Sem banco, sem nuvem, sem instalação.

  python3 agenda.py plano                      o que está atrasado, o que é hoje, o que é da semana
  python3 agenda.py add "Ligar pro contador" --ate 2026-08-20 --quem Luan --tag financeiro
  python3 agenda.py fechar "contador"          move pra Feitas com a data de hoje
  python3 agenda.py ics                        gera agenda.ics com as tarefas que têm prazo
  python3 agenda.py ler-ics dados/calendario.ics --dias 7

O arquivo de tarefas fica na raiz do workspace. Formato de uma linha:
  - [ ] o que fazer · quem · até AAAA-MM-DD · #contexto
"""

import argparse
import os
import re
import sys
from datetime import date, datetime, timedelta

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
TAREFAS = os.environ.get("ARQUIVO_TAREFAS") or os.path.join(RAIZ, "tarefas.md")

RE_TAREFA = re.compile(r"^\s*-\s*\[( |x|X)\]\s*(.+?)\s*$")
RE_DATA = re.compile(r"(\d{4}-\d{2}-\d{2})")


# ---------------------------------------------------------------- leitura

def ler():
    if not os.path.exists(TAREFAS):
        return []
    with open(TAREFAS, encoding="utf-8") as f:
        return f.read().splitlines()


def escrever(linhas):
    """Grava o arquivo garantindo uma linha em branco antes de cada '## Título'."""
    saida = []
    for linha in linhas:
        if linha.strip().startswith("##") and saida and saida[-1].strip():
            saida.append("")
        saida.append(linha)
    with open(TAREFAS, "w", encoding="utf-8") as f:
        f.write("\n".join(saida).rstrip() + "\n")


def tarefas(linhas):
    """Devolve [(indice, feita, texto, prazo)] de todas as linhas de tarefa."""
    saida = []
    for i, linha in enumerate(linhas):
        m = RE_TAREFA.match(linha)
        if not m:
            continue
        texto = m.group(2)
        d = RE_DATA.search(texto)
        prazo = None
        if d:
            try:
                prazo = datetime.strptime(d.group(1), "%Y-%m-%d").date()
            except ValueError:
                prazo = None
        saida.append((i, m.group(1).lower() == "x", texto, prazo))
    return saida


def secao(linhas, titulo):
    """Índice da linha do cabeçalho '## titulo', ou None."""
    alvo = titulo.strip().lower()
    for i, linha in enumerate(linhas):
        if linha.strip().lower().lstrip("#").strip() == alvo and linha.strip().startswith("##"):
            return i
    return None


def fim_da_secao(linhas, cabecalho):
    """Onde inserir uma linha nova dentro da seção, preservando o respiro do cabeçalho."""
    i = cabecalho + 1
    while i < len(linhas) and not linhas[i].strip().startswith("##"):
        i += 1
    while i - 1 > cabecalho and not linhas[i - 1].strip():
        i -= 1
    if i == cabecalho + 1 and i < len(linhas) and not linhas[i].strip():
        i += 1  # mantém a linha em branco logo abaixo do "## Título"
    return i


# ---------------------------------------------------------------- comandos

def cmd_plano(args):
    hoje = date.today()
    limite = hoje + timedelta(days=args.dias)
    abertas = [t for t in tarefas(ler()) if not t[1]]

    atrasadas = sorted([t for t in abertas if t[3] and t[3] < hoje], key=lambda t: t[3])
    de_hoje = [t for t in abertas if t[3] == hoje]
    semana = sorted([t for t in abertas if t[3] and hoje < t[3] <= limite], key=lambda t: t[3])
    sem_prazo = [t for t in abertas if not t[3]]

    def bloco(titulo, itens, mostrar_prazo=True):
        print("\n%s (%d)" % (titulo, len(itens)))
        if not itens:
            print("  —")
        for _, _, texto, prazo in itens:
            if mostrar_prazo and prazo:
                dias = (prazo - hoje).days
                marca = "há %dd" % -dias if dias < 0 else ("hoje" if dias == 0 else "em %dd" % dias)
                print("  · %s  [%s]" % (texto, marca))
            else:
                print("  · %s" % texto)

    print("Plano de %s" % hoje.isoformat())
    bloco("ATRASADAS", atrasadas)
    bloco("HOJE", de_hoje)
    bloco("PRÓXIMOS %d DIAS" % args.dias, semana)
    bloco("SEM PRAZO", sem_prazo, mostrar_prazo=False)
    print("\nTotal em aberto: %d" % len(abertas))
    return 0


def cmd_add(args):
    partes = [args.texto]
    if args.quem:
        partes.append(args.quem)
    if args.ate:
        partes.append("até %s" % args.ate)
    if args.tag:
        partes.append("#%s" % args.tag.lstrip("#"))
    nova = "- [ ] " + " · ".join(partes)

    linhas = ler() or ["# Tarefas", ""]
    destino = secao(linhas, args.secao)
    if destino is None:
        linhas += ["", "## %s" % args.secao, "", nova]
    else:
        linhas.insert(fim_da_secao(linhas, destino), nova)
    escrever(linhas)
    print("adicionada em '%s': %s" % (args.secao, nova))
    return 0


def cmd_fechar(args):
    linhas = ler()
    alvo = args.trecho.lower()
    achadas = [t for t in tarefas(linhas) if not t[1] and alvo in t[2].lower()]
    if not achadas:
        print("não achei tarefa aberta com: %s" % args.trecho)
        return 1
    if len(achadas) > 1 and not args.todas:
        print("achei %d tarefas com esse trecho. Seja mais específico ou use --todas:" % len(achadas))
        for _, _, texto, _ in achadas:
            print("  · %s" % texto)
        return 1

    hoje = date.today().isoformat()
    for i, _, texto, _ in achadas:
        linhas[i] = "- [x] %s · feita em %s" % (texto, hoje)
        print("fechada: %s" % texto)

    # move as fechadas pra seção Feitas, se ela existir
    if secao(linhas, "Feitas") is not None:
        movidas = [linhas[i] for i, _, _, _ in achadas]
        for i, _, _, _ in sorted(achadas, reverse=True):
            del linhas[i]
        feitas = secao(linhas, "Feitas")
        onde = fim_da_secao(linhas, feitas)
        linhas[onde:onde] = movidas
    escrever(linhas)
    return 0


def cmd_ics(args):
    """Exporta as tarefas com prazo pra um .ics que o Google/Apple Calendar importa."""
    abertas = [t for t in tarefas(ler()) if not t[1] and t[3]]
    if not abertas:
        print("nenhuma tarefa com prazo pra exportar.")
        return 1

    def escapar(texto):
        return texto.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")

    agora = datetime.now().strftime("%Y%m%dT%H%M%S")
    linhas = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Beza OS//agenda-tarefas//PT", "CALSCALE:GREGORIAN"]
    for n, (_, _, texto, prazo) in enumerate(abertas, 1):
        dia = prazo.strftime("%Y%m%d")
        linhas += [
            "BEGIN:VEVENT",
            "UID:tarefa-%d-%s@beza-os" % (n, dia),
            "DTSTAMP:%sZ" % agora,
            "DTSTART;VALUE=DATE:%s" % dia,
            "DTEND;VALUE=DATE:%s" % (prazo + timedelta(days=1)).strftime("%Y%m%d"),
            "SUMMARY:%s" % escapar(texto.split(" · ")[0]),
            "DESCRIPTION:%s" % escapar(texto),
            "END:VEVENT",
        ]
    linhas.append("END:VCALENDAR")

    destino = args.saida or os.path.join(RAIZ, "agenda.ics")
    with open(destino, "w", encoding="utf-8") as f:
        f.write("\r\n".join(linhas) + "\r\n")
    print("%d tarefas exportadas pra %s" % (len(abertas), destino))
    print("Importe esse arquivo no seu calendário (Google Agenda > Configurações > Importar).")
    return 0


def cmd_ler_ics(args):
    """Lê um .ics exportado do calendário e lista os compromissos da janela."""
    if not os.path.exists(args.arquivo):
        print("não achei o arquivo: %s" % args.arquivo)
        return 1
    with open(args.arquivo, encoding="utf-8", errors="ignore") as f:
        bruto = f.read().replace("\r\n ", "").replace("\n ", "")

    hoje = date.today()
    limite = hoje + timedelta(days=args.dias)
    eventos = []
    for bloco in bruto.split("BEGIN:VEVENT")[1:]:
        inicio = re.search(r"DTSTART[^:]*:(\d{8})", bloco)
        titulo = re.search(r"SUMMARY:(.*)", bloco)
        if not inicio:
            continue
        try:
            dia = datetime.strptime(inicio.group(1), "%Y%m%d").date()
        except ValueError:
            continue
        hora = re.search(r"DTSTART[^:]*:\d{8}T(\d{4})", bloco)
        if hoje <= dia <= limite:
            eventos.append((dia, hora.group(1) if hora else "", (titulo.group(1).strip() if titulo else "(sem título)")))

    eventos.sort()
    print("Compromissos de %s até %s (%d)" % (hoje, limite, len(eventos)))
    for dia, hora, titulo in eventos:
        marca = "%s:%s" % (hora[:2], hora[2:]) if hora else "dia inteiro"
        print("  %s  %-11s %s" % (dia.isoformat(), marca, titulo))
    if not eventos:
        print("  —")
    return 0


def main():
    p = argparse.ArgumentParser(description="Agenda e tarefas em cima de tarefas.md")
    sub = p.add_subparsers(dest="comando")

    c = sub.add_parser("plano", help="atrasadas, hoje e próximos dias")
    c.add_argument("--dias", type=int, default=7)
    c.set_defaults(func=cmd_plano)

    c = sub.add_parser("add", help="adiciona uma tarefa")
    c.add_argument("texto")
    c.add_argument("--ate", help="AAAA-MM-DD")
    c.add_argument("--quem")
    c.add_argument("--tag")
    c.add_argument("--secao", default="Em aberto")
    c.set_defaults(func=cmd_add)

    c = sub.add_parser("fechar", help="marca uma tarefa como feita")
    c.add_argument("trecho")
    c.add_argument("--todas", action="store_true")
    c.set_defaults(func=cmd_fechar)

    c = sub.add_parser("ics", help="exporta as tarefas com prazo pro calendário")
    c.add_argument("--saida")
    c.set_defaults(func=cmd_ics)

    c = sub.add_parser("ler-ics", help="lê um .ics do calendário e lista os compromissos")
    c.add_argument("arquivo")
    c.add_argument("--dias", type=int, default=7)
    c.set_defaults(func=cmd_ler_ics)

    args = p.parse_args()
    if not args.comando:
        p.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
