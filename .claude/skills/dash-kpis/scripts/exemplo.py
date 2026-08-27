#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Popula o painel com dados de exemplo, pra você ver como fica antes de colocar os seus.

  python3 exemplo.py          cria um banco de demonstração em financeiro/dash-exemplo.db
  python3 exemplo.py --aqui   escreve no banco de verdade (só se ele estiver vazio)
"""

import os
import sys
from datetime import date, timedelta

if "--aqui" not in sys.argv:
    os.environ.setdefault(
        "DASH_DB",
        os.path.join(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")),
            "financeiro", "dash-exemplo.db",
        ),
    )

import nucleo  # noqa: E402  (o env acima precisa vir antes)


def main():
    con = nucleo.conectar()
    if con.execute("SELECT COUNT(*) n FROM clientes").fetchone()["n"] > 0:
        print("Já tem dado nesse banco. Nada foi alterado.")
        print("Banco: %s" % nucleo.BANCO)
        return 0

    nucleo.definir_config(con, "negocio", "Empresa Exemplo")
    nucleo.definir_config(con, "meta_recorrente", 30000)
    nucleo.definir_config(con, "meta_faturamento_mes", 35000)
    nucleo.definir_config(con, "custo_fixo_mes", 12000)

    hoje = date.today()
    clientes = [
        ("Padaria do Bairro", 2500, 240),
        ("Clínica Vida", 4800, 180),
        ("Marcenaria Silva", 3200, 120),
        ("Auto Peças Norte", 1800, 90),
        ("Estúdio Fotográfico Luz", 2200, 45),
        ("Construtora Horizonte", 6500, 20),
    ]
    for nome, valor, dias in clientes:
        nucleo.add_cliente(con, nome, valor, "recorrente", (hoje - timedelta(days=dias)).isoformat())
        for m in range(3):
            data = (hoje.replace(day=1) - timedelta(days=30 * m)).isoformat()
            nucleo.receber(con, nome, valor, data, "mensalidade")

    nucleo.add_cliente(con, "Restaurante Maré", 2000, "recorrente", (hoje - timedelta(days=300)).isoformat())
    nucleo.churn(con, "Restaurante Maré", "trocou por sobrinho que faz mais barato",
                 (hoje - timedelta(days=25)).isoformat())

    leads = [
        ("Joana Ribeiro", "Clínica Sorriso", 3500, "indicacao", "proposta"),
        ("Marcos Tavares", "Transportes MT", 5200, "instagram", "negociacao"),
        ("Ana Paula", "Boutique Ana", 1800, "indicacao", "conversa"),
        ("Rogério Lima", "Academia Força", 2800, "prospeccao", "novo"),
        ("Carla Mendes", "Pet Shop Amigo", 1500, "instagram", "novo"),
    ]
    for nome, empresa, ticket, origem, estagio in leads:
        nucleo.add_lead(con, nome, empresa, ticket, origem)
        if estagio != "novo":
            nucleo.mover_lead(con, nome, estagio)

    print(nucleo.resumo_texto(nucleo.resumo(con)))
    print("\nBanco de exemplo: %s" % nucleo.BANCO)
    print("Pra ver no painel:  DASH_DB=\"%s\" ./start.sh" % nucleo.BANCO)
    return 0


if __name__ == "__main__":
    sys.exit(main())
