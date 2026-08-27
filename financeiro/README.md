# financeiro/

Onde o dinheiro do negócio é registrado e lido. Três skills trabalham aqui:

| Skill | O que faz |
|---|---|
| `/dash-kpis` | painel local com receita, carteira, funil e meta. Roda no navegador, sem internet |
| `/fechamento-mes` | fecha o mês e escreve `fechamentos/AAAA-MM.md` |
| `/fluxo-caixa` | projeta 90 dias e mostra qual mês fica no vermelho |

## Os arquivos

- `clientes-fees.md` — quem paga quanto, quando, e em qual pacote. **Fonte de verdade da receita recorrente.**
- `metas.md` — quanto você quer faturar e até quando.
- `custos.md` — o que sai todo mês, fixo e variável.
- `fechamentos/` — um arquivo por mês fechado. Histórico que ninguém reescreve.
- `dash.db` — banco do painel, criado na primeira vez que você roda `/dash-kpis`. Fica só na sua máquina, nunca vai pro GitHub.

## A regra de ouro

Não existe número em dois lugares. Se quem é cliente e quanto paga está em `clientes-fees.md`, nenhuma outra planilha manda nisso. Quando o painel e o arquivo divergirem, o arquivo ganha e o painel se corrige.

## Isso não é contabilidade

Aqui é gestão: você olhando os seus números pra decidir. Nota fiscal, imposto e obrigação acessória continuam com o seu contador.
