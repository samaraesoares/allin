#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Servidor do painel. Roda local, sem internet, sem instalar nada.

  python3 server.py           abre em http://localhost:8765
  python3 server.py 9000      escolhe outra porta
"""

import json
import os
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

import nucleo

AQUI = os.path.dirname(os.path.abspath(__file__))
PORTA = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("DASH_PORTA", 8765))


class Painel(BaseHTTPRequestHandler):

    # ------------------------------------------------------------ utilidades
    def responder(self, corpo, tipo="application/json; charset=utf-8", status=200):
        dados = corpo.encode("utf-8") if isinstance(corpo, str) else corpo
        self.send_response(status)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(dados)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(dados)

    def corpo_json(self):
        tamanho = int(self.headers.get("Content-Length") or 0)
        if not tamanho:
            return {}
        try:
            return json.loads(self.rfile.read(tamanho).decode("utf-8"))
        except ValueError:
            return {}

    def erro(self, mensagem, status=400):
        self.responder(json.dumps({"erro": mensagem}, ensure_ascii=False), status=status)

    def log_message(self, *args):
        pass  # sem ruído no terminal

    # ------------------------------------------------------------ rotas
    def do_GET(self):
        caminho = self.path.split("?")[0]

        if caminho in ("/", "/index.html"):
            with open(os.path.join(AQUI, "painel.html"), "rb") as f:
                return self.responder(f.read(), "text/html; charset=utf-8")

        if caminho == "/api/painel":
            con = nucleo.conectar()
            return self.responder(json.dumps(nucleo.resumo(con), ensure_ascii=False, default=str))

        if caminho == "/api/resumo.md":
            con = nucleo.conectar()
            return self.responder(nucleo.resumo_texto(nucleo.resumo(con)), "text/plain; charset=utf-8")

        return self.erro("rota não encontrada", 404)

    def do_POST(self):
        caminho = self.path.split("?")[0]
        dados = self.corpo_json()
        con = nucleo.conectar()

        try:
            if caminho == "/api/clientes":
                nucleo.add_cliente(con, dados["nome"], dados.get("valor", 0),
                                   dados.get("tipo", "recorrente"), dados.get("entrada"))
            elif caminho == "/api/churn":
                nucleo.churn(con, dados["nome"], dados.get("motivo"))
            elif caminho == "/api/recebimentos":
                nucleo.receber(con, dados["cliente"], dados["valor"], dados.get("data"), dados.get("descricao"))
            elif caminho == "/api/leads":
                nucleo.add_lead(con, dados["nome"], dados.get("empresa"),
                                dados.get("ticket", 0), dados.get("origem", "outro"))
            elif caminho == "/api/mover":
                nucleo.mover_lead(con, dados["nome"], dados["estagio"], dados.get("valor"))
            elif caminho == "/api/config":
                for chave, valor in dados.items():
                    nucleo.definir_config(con, chave, valor)
            elif caminho == "/api/fechar-mes":
                nucleo.fechar_mes(con, dados.get("mes"))
            else:
                return self.erro("rota não encontrada", 404)
        except KeyError as e:
            return self.erro("faltou o campo %s" % e)
        except ValueError as e:
            return self.erro(str(e))

        return self.responder(json.dumps(nucleo.resumo(con), ensure_ascii=False, default=str))


def main():
    nucleo.conectar()  # cria o banco na primeira execução
    servidor = HTTPServer(("127.0.0.1", PORTA), Painel)
    url = "http://localhost:%d" % PORTA
    print("Painel no ar: %s" % url)
    print("Banco: %s" % nucleo.BANCO)
    print("Pra parar: Ctrl+C")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nPainel fechado.")


if __name__ == "__main__":
    main()
