---
name: fluxo-caixa
description: >
  Projeção de caixa de 90 dias a partir dos fees recorrentes, dos projetos a receber e dos
  custos fixos, variáveis e anuais. Aponta em qual mês o caixa fica no vermelho, de quanto é o
  buraco e o que segura ele. Também responde "posso contratar?" e "posso comprar isso?".
  Use quando o usuário chamar /fluxo-caixa, ou disser "projeção de caixa", "vou ter dinheiro
  em", "posso contratar alguém", "dá pra comprar", "quanto sobra por mês", "meu caixa aguenta",
  "quanto tempo eu aguento sem vender", "vou fechar no vermelho".
---

# /fluxo-caixa — os próximos 90 dias

## O que essa skill responde

Três perguntas que decidem quase tudo em empresa pequena:

1. **Em qual mês o caixa aperta?**
2. **Quanto tempo eu aguento se não entrar mais nada?**
3. **Posso assumir esse custo novo?**

Não é contabilidade. É a conta que o dono precisa ter na cabeça e quase nunca tem escrita.

## As fontes

- `financeiro/clientes-fees.md` — recorrente e projetos a receber, com data
- `financeiro/custos.md` — fixos, pessoas, variáveis e os **anuais** (esses são os que derrubam o mês)
- `financeiro/metas.md` — pró-labore e ponto de equilíbrio
- Banco do `/dash-kpis` — histórico de recebimento real, pra calibrar o quanto atrasa na prática

Faltando o saldo em conta hoje, pergunte. Sem ele a projeção é relativa, não absoluta.

## O fluxo

### 1. Perguntar o que só o usuário sabe

Junto, em uma pergunta só:

> "Pra projetar preciso de três coisas: quanto você tem em caixa hoje, se tem alguma entrada grande já contratada nos próximos 3 meses, e se tem alguma saída grande prevista (imposto, 13º, equipamento, viagem)."

### 2. Montar a projeção

Mês a mês, três meses à frente:

```
Saldo inicial
+ recorrente previsto        (dos fees ativos, descontando o que costuma atrasar)
+ projetos a receber         (só o que está contratado, nunca o que está em proposta)
− custo fixo
− pessoas
− variáveis                  (média dos últimos meses)
− anuais que caem no mês     (o que mais pega de surpresa)
= saldo final                → vira o saldo inicial do mês seguinte
```

**Regra de conservadorismo:** entrada só entra quando está contratada. Proposta enviada não é receita, é esperança. Custo, ao contrário, entra sempre pelo teto. Projeção que erra pra cima é pior do que não ter projeção.

### 3. Entregar

Uma tabela e três frases:

```markdown
| Mês | Entra | Sai | Saldo no fim |
|---|---|---|---|
| AAAA-MM | R$ 0,00 | R$ 0,00 | R$ 0,00 |
| AAAA-MM | R$ 0,00 | R$ 0,00 | R$ 0,00 |
| AAAA-MM | R$ 0,00 | R$ 0,00 | R$ 0,00 |
```

Depois:

- **Fôlego:** "sem entrar nada novo, o caixa aguenta X meses."
- **O mês do aperto:** qual e por quê (quase sempre é anual caindo junto com mês fraco).
- **O que resolve:** o número exato de venda nova, ou o corte, que tira o mês do vermelho. Não "vender mais": "um cliente de R$ 3.000 assinando até o dia 20".

Salve em `financeiro/projecao-AAAA-MM.md` se o usuário quiser guardar.

## "Posso contratar?"

Não responda com opinião. Rode a conta:

1. Custo real da pessoa (salário + encargos + ferramentas + o tempo de quem treina). Para CLT no Brasil, aproxime o custo total em 1,7x o salário e diga que é aproximação.
2. Some ao custo fixo e rode a projeção de novo.
3. Responda com o limiar: **quanto de recorrente novo precisa existir, e até quando, pra essa contratação não comer a reserva.**

A resposta boa tem esta forma: "dá, se o recorrente chegar a R$ X até [mês]; hoje está em R$ Y."

## Regras

- **Nunca conte proposta como receita.** Nem "praticamente fechada".
- **Custo anual esquecido é o assassino número 1** de caixa de empresa pequena. Sempre pergunte por imposto anual, 13º, férias, seguro e renovação de licença.
- **Reserva:** o padrão saudável é 3 meses de custo fixo parado. Se ele não tem, diga onde está e qual é a meta, sem sermão.
- **Não dê conselho de investimento.** Aqui é caixa operacional. Se ele perguntar onde aplicar a reserva, diga que isso é conversa com o contador ou assessor dele.
- Se os arquivos de `financeiro/` estiverem vazios, não simule. Preencha com ele primeiro: 15 minutos de cadastro valem mais do que uma projeção inventada.
