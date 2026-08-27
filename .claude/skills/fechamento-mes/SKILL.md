---
name: fechamento-mes
description: >
  Fecha o mês do negócio: faturado, receita recorrente, quem entrou, quem saiu, comparação com
  a meta e a leitura do que aconteceu. Grava a fotografia no painel e escreve o arquivo em
  financeiro/fechamentos/AAAA-MM.md.
  Use quando o usuário chamar /fechamento-mes, ou disser "fecha o mês", "como foi o mês",
  "resultado do mês", "bati a meta?", "quanto entrou esse mês", "fechamento", "comparar com o
  mês passado", "relatório do mês".
---

# /fechamento-mes — a fotografia do mês

## Por que isso existe

Sem fechamento, todo mês parece igual: sempre corrido, sempre "deu pra pagar as contas". O fechamento congela o número e transforma sensação em série histórica. É o que permite dizer "caiu" ou "subiu" com alguma autoridade.

Leva dez minutos. Roda uma vez por mês, no último dia útil.

## As fontes

Nesta ordem, e nenhuma outra:

1. `financeiro/clientes-fees.md` — quem é cliente e quanto paga (a verdade sobre o recorrente)
2. `financeiro/custos.md` — o que sai
3. `financeiro/metas.md` — o que era pra ter acontecido
4. O banco do `/dash-kpis` — recebimentos e movimento do mês
5. O fechamento anterior em `financeiro/fechamentos/` — pra comparar

Se as fontes divergirem, **o arquivo markdown ganha do banco**, e você corrige o banco. Nunca o contrário.

## O fluxo

### 1. Levantar

```bash
cd .claude/skills/dash-kpis/scripts
python3 cli.py resumo
```

Leia também `clientes-fees.md` e o fechamento do mês anterior.

### 2. Conferir com o usuário antes de gravar

Fechamento errado vira histórico errado pra sempre. Pergunte, de forma direta e junta (não uma por vez):

- "Entrou algum cliente esse mês que ainda não está no sistema?"
- "Saiu alguém? Por qual motivo, de verdade?"
- "Recebeu algo fora do recorrente: projeto, avulso, atrasado que caiu agora?"
- "Teve custo grande fora do normal?"

Registre o que ele responder no painel (`cli.py cliente`, `cli.py churn`, `cli.py receber`) **antes** de fechar.

### 3. Gravar

```bash
python3 cli.py fechar-mes
```

### 4. Escrever o arquivo

Em `financeiro/fechamentos/AAAA-MM.md`, neste formato:

```markdown
# Fechamento — [mês de AAAA]

**Fechado em:** AAAA-MM-DD

## Números

| Indicador | Este mês | Mês anterior | Variação |
|---|---|---|---|
| Faturado | R$ 0,00 | R$ 0,00 | +0% |
| Recorrente no fim do mês | R$ 0,00 | R$ 0,00 | +0% |
| Custo fixo | R$ 0,00 | R$ 0,00 | |
| Sobra | R$ 0,00 | R$ 0,00 | |
| Clientes ativos | 0 | 0 | |
| Ticket médio | R$ 0,00 | R$ 0,00 | |

## Meta

Meta do mês: R$ 0,00. Realizado: R$ 0,00. [Bateu / faltou R$ X.]

## Movimento

**Entraram:** [nome, valor, de onde veio o lead]
**Saíram:** [nome, valor, motivo real]

## Leitura

[Três a cinco linhas. O que explica o número, não o número de novo.]

## O que muda no mês que vem

- [decisão concreta, com dono e prazo]
```

### 5. Devolver a leitura na conversa

Mostre a tabela e três frases de leitura. Depois jogue as decisões que saíram daí em `tarefas.md` (a skill `/agenda-tarefas` faz isso).

## O que olhar na leitura

O trabalho de verdade está aqui. Cheque, nesta ordem:

1. **Sobra sobre o custo fixo.** Se está negativa, é o único assunto do fechamento. Fale disso primeiro e proponha o corte ou a venda que resolve.
2. **Concentração.** Se um cliente é mais de 40% do recorrente, o negócio é refém. Diga o número e proponha meta de diluição.
3. **Motivo das saídas.** Duas saídas pelo mesmo motivo em três meses é padrão, não coincidência. Nomeie o padrão.
4. **De onde vieram as entradas.** Se todas vieram de indicação, não existe canal, existe sorte com prazo de validade.
5. **Recorrente contra faturado.** Faturado alto com recorrente parado significa mês salvo por projeto avulso. Isso não se repete sozinho.

## Regras

- **Fechado é fechado.** Não reescreva fechamento anterior. Erro descoberto depois vira nota no mês corrente.
- **Não maquie.** Se o mês foi ruim, o arquivo diz que foi ruim. O valor dessa série é ela ser confiável.
- **Motivo de saída sempre real.** "Questões internas do cliente" não ensina nada. "Achou caro porque não viu resultado em 3 meses" ensina.
- Não invente comparação se não existe mês anterior. No primeiro fechamento, diga que ele é a linha de base.
