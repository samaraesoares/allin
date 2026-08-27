---
name: agenda-tarefas
description: >
  Captura, organiza e fecha tarefa em cima de tarefas.md, e monta o plano do dia e da semana
  com o que está atrasado, o que vence hoje e o que vem depois. Puxa tarefa de reunião, de
  áudio e de conversa solta. Exporta prazo pro calendário (.ics) e lê agenda exportada, sem
  precisar de nenhuma integração instalada.
  Use quando o usuário chamar /agenda-tarefas, ou disser "o que eu tenho pra hoje", "plano da
  semana", "minhas tarefas", "o que está atrasado", "anota aí", "lembra de", "põe na lista",
  "terminei o X", "já fiz isso", "tira essa tarefa", "o que saiu dessa reunião", "joga pro
  calendário", "o que tenho na agenda".
---

# /agenda-tarefas — o dia organizado

## O princípio

Uma lista só, em texto puro: `tarefas.md`, na raiz do workspace. Sem app, sem login, sem sincronização pra dar errado. Você lê e escreve nesse arquivo; o script cuida do formato.

Formato de uma linha:

```
- [ ] o que fazer · quem · até AAAA-MM-DD · #contexto
```

Só "o que fazer" é obrigatório. Data sempre em AAAA-MM-DD, senão a ordenação mente.

## Os comandos

Rode a partir de `.claude/skills/agenda-tarefas/scripts/`:

```bash
python3 agenda.py plano                    # atrasadas, hoje, próximos 7 dias, sem prazo
python3 agenda.py plano --dias 15
python3 agenda.py add "Ligar pro contador" --ate 2026-08-20 --quem Luan --tag financeiro
python3 agenda.py add "Revisar orçamento" --secao Hoje
python3 agenda.py fechar "contador"        # acha pelo trecho e move pra Feitas com a data
python3 agenda.py ics                      # exporta os prazos pro calendário
python3 agenda.py ler-ics dados/agenda.ics --dias 7
```

Editar o `tarefas.md` na mão também vale. O script não é dono do arquivo, é conveniência.

## Como usar na conversa

### "O que eu tenho pra hoje?"

Rode `plano` e responda **em três blocos, nessa ordem**: atrasadas, hoje, e o que vem. Depois acrescente uma linha de leitura, que é o que o script não faz:

- Se tem mais de 5 atrasadas, o problema não é organização, é volume. Diga isso e pergunte o que pode morrer.
- Se tudo está sem prazo, a lista é um depósito, não um plano. Ofereça colocar data nas três mais importantes.
- Termine sempre perguntando por onde começar, não repetindo a lista.

### "Anota aí que preciso ligar pro contador"

Adicione na hora, sem perguntar detalhe demais. Se ele deu prazo, use `--ate`. Se não deu, não invente: tarefa sem prazo é honesta, tarefa com prazo inventado é ruído. Só pergunte a data se a tarefa claramente depender dela.

### "Terminei o X"

`fechar` com um trecho do texto. Se o trecho bater em mais de uma tarefa, o script para e lista as candidatas — mostre elas e pergunte qual.

### Depois de uma reunião

Ao escrever uma ata em `reunioes/`, **puxe as tarefas de lá pra cá**, uma por linha, com responsável e prazo. Ata cheia de combinado e lista vazia é o jeito mais comum de perder trabalho combinado.

### Calendário, sem integração

O aluno não precisa de MCP no dia 1:

- **Levar tarefa pro calendário:** `agenda.py ics` gera `agenda.ics` na raiz. No Google Agenda: Configurações > Importar. No Apple Calendário: duplo clique no arquivo.
- **Trazer o calendário pra cá:** o usuário exporta a agenda dele (Google Agenda > Configurações > Importar e exportar > Exportar), joga o `.ics` em `dados/` e você lê com `ler-ics`. Assim você consegue dizer "você tem reunião às 15h, essa tarefa não cabe hoje".

Se ele tiver o MCP de Google Agenda instalado, use o MCP e ignore o `.ics`. Detecte, não pergunte.

## O plano da semana

Quando ele pedir o plano da semana, não jogue a lista inteira. Faça assim:

1. Rode `plano --dias 7`
2. Agrupe por contexto (`#tag`) ou por cliente, não por data
3. Aponte o conflito: dia com três coisas grandes é dia que não vai acontecer
4. Proponha **três** prioridades pra semana. Só três. Uma lista de 15 prioridades não tem nenhuma

## Regras

- **Não crie tarefa que o usuário não pediu.** Sugerir é bom; cadastrar por conta própria enche a lista de coisa que ninguém vai fazer.
- **Prazo é do usuário.** Só sugira data quando ele pedir ajuda pra decidir.
- **Fechar é rápido, não cerimonioso.** Marcou como feita, confirme em uma linha e siga.
- **Não mova a estrutura do arquivo.** As seções (`## Hoje`, `## Esta semana`, `## Em aberto`, `## Feitas`) são o contrato com o usuário.
- Tarefa que aparece atrasada há mais de 30 dias não é tarefa, é decisão adiada. Uma vez por mês, ofereça matar essas.

## Arquivos

- [scripts/agenda.py](scripts/agenda.py) — plano, adicionar, fechar, exportar e ler calendário
