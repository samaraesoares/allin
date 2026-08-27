#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Linha de comando do painel. É por aqui que o Claude registra as coisas na conversa.

Exemplos:
  python3 cli.py config negocio "Marcenaria Silva"
  python3 cli.py config meta_recorrente 30000
  python3 cli.py cliente "Padaria do Bairro" --valor 2500
  python3 cli.py receber "Padaria do Bairro" --valor 2500
  python3 cli.py churn "Padaria do Bairro" --motivo "cortou marketing"
  python3 cli.py lead "Joana" --empresa "Clínica Vida" --ticket 3500 --origem indicacao
  python3 cli.py mover "Joana" --para proposta
  python3 cli.py mover "Joana" --para fechado --valor 3200
  python3 cli.py resumo
  python3 cli.py fechar-mes
"""

import argparse
import sys

import nucleo


def main():
    p = argparse.ArgumentParser(description="Painel de KPIs do negócio")
    sub = p.add_subparsers(dest="comando")

    c = sub.add_parser("config", help="lê ou define uma configuração")
    c.add_argument("chave", nargs="?")
    c.add_argument("valor", nargs="?")

    c = sub.add_parser("cliente", help="cadastra ou atualiza um cliente")
    c.add_argument("nome")
    c.add_argument("--valor", default=0)
    c.add_argument("--tipo", default="recorrente", choices=["recorrente", "projeto"])
    c.add_argument("--entrada")
    c.add_argument("--nota")

    c = sub.add_parser("churn", help="marca a saída de um cliente")
    c.add_argument("nome")
    c.add_argument("--motivo")
    c.add_argument("--data")

    c = sub.add_parser("receber", help="registra um recebimento")
    c.add_argument("cliente")
    c.add_argument("--valor", required=True)
    c.add_argument("--data")
    c.add_argument("--descricao")

    c = sub.add_parser("lead", help="cadastra um lead no funil")
    c.add_argument("nome")
    c.add_argument("--empresa")
    c.add_argument("--ticket", default=0)
    c.add_argument("--origem", default="outro")
    c.add_argument("--nota")

    c = sub.add_parser("mover", help="move um lead de estágio")
    c.add_argument("nome")
    c.add_argument("--para", required=True, choices=nucleo.ESTAGIOS)
    c.add_argument("--valor")
    c.add_argument("--nota")

    sub.add_parser("resumo", help="mostra o resumo em markdown")

    c = sub.add_parser("fechar-mes", help="grava a fotografia do mês")
    c.add_argument("--mes", help="AAAA-MM (padrão: mês corrente)")

    args = p.parse_args()
    if not args.comando:
        p.print_help()
        return 0

    con = nucleo.conectar()

    if args.comando == "config":
        if args.chave and args.valor is not None:
            nucleo.definir_config(con, args.chave, args.valor)
            print("%s = %s" % (args.chave, args.valor))
        else:
            for chave, valor in sorted(nucleo.config(con).items()):
                print("%-24s %s" % (chave, valor))

    elif args.comando == "cliente":
        linha = nucleo.add_cliente(con, args.nome, args.valor, args.tipo, args.entrada, args.nota)
        print("cliente salvo: %s · %s · %s" % (linha["nome"], linha["valor"], linha["tipo"]))

    elif args.comando == "churn":
        n = nucleo.churn(con, args.nome, args.motivo, args.data)
        print("saída registrada" if n else "não achei cliente com esse nome: %s" % args.nome)

    elif args.comando == "receber":
        nucleo.receber(con, args.cliente, args.valor, args.data, args.descricao)
        print("recebimento registrado: %s · %s" % (args.cliente, args.valor))

    elif args.comando == "lead":
        i = nucleo.add_lead(con, args.nome, args.empresa, args.ticket, args.origem, args.nota)
        print("lead #%s criado: %s" % (i, args.nome))

    elif args.comando == "mover":
        try:
            lead = nucleo.mover_lead(con, args.nome, args.para, args.valor, args.nota)
        except ValueError as e:
            print(str(e))
            return 1
        print("%s → %s" % (lead["nome"], args.para))

    elif args.comando == "resumo":
        print(nucleo.resumo_texto(nucleo.resumo(con)))

    elif args.comando == "fechar-mes":
        r = nucleo.fechar_mes(con, args.mes)
        print(nucleo.resumo_texto(r))
        print("\nMês %s fechado e gravado." % r["mes"])

    return 0


if __name__ == "__main__":
    sys.exit(main())
