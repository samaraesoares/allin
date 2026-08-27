---
name: dash-kpis
description: >
  Painel de KPIs do negócio: receita recorrente contra a meta, faturado do mês, carteira de
  clientes, entradas e saídas, ticket médio, concentração, funil de vendas e histórico de meses
  fechados. Roda local no navegador (Python + SQLite, zero instalação, zero internet) e também
  responde na conversa, sem abrir o painel.
  Use quando o usuário chamar /dash-kpis, ou disser "como está o mês", "quanto eu tenho de
  recorrente", "abre o painel", "meus números", "quanto faturei", "quantos clientes ativos",
  "como está a meta", "cadastra o cliente X", "fulano fechou", "fulano saiu", "registra o
  recebimento", "manda proposta pro fulano", "como está o funil", "quanto tem no pipeline".
---

# /dash-kpis — o painel do negócio

## O que essa skill é

Um painel local com os números que decidem o mês. Roda com o Python que já vem no computador, guarda tudo em um arquivo SQLite dentro do próprio workspace (`financeiro/dash.db`) e não manda nada pra lugar nenhum.

Duas formas de usar, e as duas mexem no mesmo banco:

1. **Na conversa.** O usuário fala, você registra e responde com o número. É o uso do dia a dia.
2. **No navegador.** `./start.sh` abre o painel visual. É o uso do ritual de sexta.

## Antes de qualquer coisa

Os scripts ficam em `.claude/skills/dash-kpis/scripts/`. Rode sempre a partir dessa pasta:

```bash
cd .claude/skills/dash-kpis/scripts
```

Na primeira execução o banco é criado sozinho. Não existe passo de instalação.

## Primeira vez: configurar

Se `config` ainda estiver no padrão (negócio "Meu negócio", metas zeradas), pergunte antes de mostrar qualquer número:

1. "Qual o nome do negócio?"
2. "Quanto você quer ter de receita recorrente por mês?"
3. "Quanto sai de custo fixo todo mês?" (se ele não souber, ler `financeiro/custos.md`)

E grave:

```bash
python3 cli.py config negocio "Marcenaria Silva"
python3 cli.py config meta_recorrente 30000
python3 cli.py config custo_fixo_mes 12000
python3 cli.py config meta_faturamento_mes 35000
```

Depois puxe o que já existe em `financeiro/clientes-fees.md` e cadastre a carteira de uma vez, sem pedir pro usuário digitar de novo. Ele já escreveu isso uma vez.

## Registrar, na conversa

| O usuário diz | Você roda |
|---|---|
| "fechei com a Clínica Vida, 4.800 por mês" | `python3 cli.py cliente "Clínica Vida" --valor 4800` |
| "a Padaria me pagou hoje" | `python3 cli.py receber "Padaria do Bairro" --valor 2500` |
| "a Padaria cancelou" | `python3 cli.py churn "Padaria do Bairro" --motivo "cortou marketing"` |
| "entrou um lead, Joana da Clínica Sorriso, uns 3.500" | `python3 cli.py lead "Joana" --empresa "Clínica Sorriso" --ticket 3500 --origem indicacao` |
| "mandei proposta pra Joana" | `python3 cli.py mover "Joana" --para proposta` |
| "a Joana fechou por 3.200" | `python3 cli.py mover "Joana" --para fechado --valor 3200` |
| "a Joana sumiu" | `python3 cli.py mover "Joana" --para perdido` |

Estágios do funil: `novo`, `conversa`, `proposta`, `negociacao`, `fechado`, `perdido`. Mover pra `fechado` com valor **já cria o cliente na carteira** — não cadastre duas vezes.

**Sempre confirme o motivo da saída.** "A Padaria cancelou" sem motivo é dado morto; com motivo, três saídas iguais viram um defeito identificável no serviço.

## Ler os números

```bash
python3 cli.py resumo
```

Devolve a tabela pronta em markdown. Cole na conversa e **acrescente a leitura**, que é a parte que o script não faz. Números sem leitura não mudam decisão. O que olhar:

- **Sobra sobre o fixo negativa:** o recorrente não paga a casa. É a informação mais urgente do painel, fale dela primeiro.
- **Concentração acima de 40%:** um cliente só banca quase tudo. Se ele sair, o mês vira. Diga isso.
- **Taxa de fechamento:** propostas no mês contra fechamentos. Baixa demais é problema de qualificação, não de volume.
- **Entradas contra saídas:** carteira que cresce em receita mas encolhe em clientes é concentração aumentando disfarçada de crescimento.

## Abrir o painel visual

```bash
./start.sh
```

Abre em http://localhost:8765 e o navegador sozinho. Windows: `start.bat` (duplo clique também funciona). Pra parar: Ctrl+C no terminal.

O painel tem um formulário de registro embutido, pro usuário lançar sem passar por você.

## Fechar o mês

```bash
python3 cli.py fechar-mes
```

Grava a fotografia do mês (faturado, recorrente, clientes, entradas, saídas) na tabela de fechamentos. É o que faz a comparação entre meses existir. Rode no último dia útil.

A skill `/fechamento-mes` faz isso **e** escreve o arquivo em `financeiro/fechamentos/`. Se o usuário estiver fechando o mês de verdade, use ela, não este comando solto.

## Ver funcionando antes de ter dados

```bash
python3 exemplo.py
```

Cria um banco de demonstração separado (`financeiro/dash-exemplo.db`) com uma carteira fictícia, pra mostrar o painel cheio. Não toca no banco de verdade.

```bash
DASH_DB="$PWD/../../../../financeiro/dash-exemplo.db" ./start.sh
```

## Regras

- **O arquivo manda no painel.** Se `financeiro/clientes-fees.md` e o banco divergirem, o arquivo está certo e o banco se corrige. Nunca o contrário.
- **Não invente número.** Se o dado não está no banco, diga que não está e pergunte.
- **Não commite o banco.** `financeiro/dash.db` já está no `.gitignore` — os números são do usuário e ficam na máquina dele.
- **Um comando por fato.** Registre na hora em que o usuário conta, não no fim da conversa. Fato registrado tarde vira fato esquecido.
- Se o Python não estiver instalado (raro no Mac, comum no Windows), o `start.sh` explica onde baixar. Não tente contornar com outra linguagem.

## Arquivos

- [scripts/nucleo.py](scripts/nucleo.py) — banco, regras e cálculos
- [scripts/cli.py](scripts/cli.py) — a linha de comando que você usa na conversa
- [scripts/server.py](scripts/server.py) — servidor local do painel
- [scripts/painel.html](scripts/painel.html) — a interface
- [scripts/exemplo.py](scripts/exemplo.py) — banco de demonstração
- [scripts/start.sh](scripts/start.sh) / [scripts/start.bat](scripts/start.bat) — abrir o painel
