---
name: setup
description: >
  Configura o Beza OS pro negócio de quem instalou. Faz perguntas sobre quem é a pessoa, o que
  a empresa vende e como ela trabalha, e a partir disso escreve o AGENTS.md, os arquivos de
  contexto, o guia de marca, adapta a estrutura de pastas e sugere os conectores que fazem
  sentido. É o primeiro comando a rodar depois de instalar.
  Use quando o usuário chamar /setup, quando _contexto/empresa.md estiver vazio ou ausente, ou
  quando disser "configurar o sistema", "primeira vez", "setup", "acabei de instalar".
---

# /setup — configuração do sistema

## Passo 0 — Ambiente (silencioso, antes de tudo)

O sistema serve Claude Code e Codex. Antes das perguntas, garanta que os dois enxergam as skills.
Faça sem alardear: é setup técnico. Só reporte se falhar.

**Criar a ponte `.agents/skills`, apontando pra `.claude/skills`.** Sempre criar, independente do
agente que está rodando agora — a pessoa pode abrir no outro amanhã.

```bash
# Mac / Linux — nunca no Windows, mesmo em Git Bash (ln -s falha silenciosamente sem
# privilégio elevado e cai pra cópia, mesmo reportando "symlink criado")
bash scripts/sync-ponte.sh
```
```powershell
# Windows — sempre este, mesmo se a sessão está em Git Bash. É o único que tenta
# junction (não exige privilégio nem Developer Mode e é link de verdade)
powershell -ExecutionPolicy Bypass -File scripts\sync-ponte.ps1
```

Detecte o sistema pelo ambiente: se `uname` responder `Linux` ou `Darwin`, use o `.sh`; em qualquer
cenário Windows (incluindo Git Bash, onde `uname` responde `MINGW*`/`MSYS*`), use sempre o `.ps1`.
O script é idempotente. Quando a ponte cai pra cópia (Windows sem junction), skill nova precisa
re-sincronizar — o `/mapear` e o `/atualizar` rodam esse mesmo script no fim.

---

## Verificação inicial

Veja se `_contexto/empresa.md` já tem conteúdo real (não o template).

- **Vazio ou ausente:** siga o onboarding abaixo.
- **Já preenchido:** avise que o setup já foi feito e pergunte se quer refazer do zero ou atualizar só uma parte.

---

## Onboarding

Abra curto:

> "Boa. Vou te fazer algumas perguntas pra configurar o sistema pro seu negócio. Responde com calma: quanto mais específico, melhor o sistema trabalha pra ti."

Perguntas **uma por vez**, em conversa natural. Nunca despeje a lista toda.

### 1. Nome e negócio

"Qual é o seu nome e o nome da sua empresa?"

Guarde os dois separados. Eles viram nome de pasta mais pra frente.

### 2. Histórico

"Você já usa o Claude Code há algum tempo, ou é a primeira vez?"

**Se já usa:** "Quer que eu tente carregar o que você já tem configurado em outros projetos, ou prefere configurar do zero aqui?" Se quiser carregar, siga o bloco **Carregar contexto existente**.

**Se é a primeira vez:** "Você usa outro assistente de IA com frequência, tipo ChatGPT ou Gemini? Se sim, consigo puxar o contexto de lá pra você não responder tudo de novo." Se usa, siga o bloco **Importar de outro assistente**.

#### Bloco: carregar contexto existente

Tente ler, nesta ordem:
1. `~/.claude/CLAUDE.md`
2. Arquivos de memória em `~/.claude/projects/`

Monte um resumo do que achou (nome, negócio, o que faz, tom de voz, ferramentas) e peça confirmação. Depois **pule as perguntas já respondidas**. Se não achar nada, diga isso em uma linha e siga.

#### Bloco: importar de outro assistente

Mostre este prompt pro usuário copiar:

```
Preciso exportar o contexto do meu negócio das nossas conversas para configurar uma nova ferramenta. Responda com o que você sabe sobre mim nestas categorias, deixando em branco o que não souber:

NOME:
EMPRESA:
O QUE A EMPRESA FAZ:
PRINCIPAIS ATIVIDADES DO MEU DIA:
CLIENTES:
EQUIPE:
FERRAMENTAS QUE USO:
IDENTIDADE VISUAL:
TOM DE VOZ:
O QUE EVITAR NA ESCRITA:
OUTROS DETALHES:
```

Peça pra ele colar a resposta aqui, extraia tudo, confirme e pule as perguntas já cobertas.

### 3. O que a empresa faz

"O que sua empresa vende, e pra quem?"

### 4. O dia a dia

"O que você mais produz ou resolve no dia a dia? Pode ser mais de uma coisa."

### 5. Clientes

"Você atende clientes externos, ou o sistema é pro seu próprio negócio?"

### 6. Foco atual

"Qual é o seu foco agora? O que você está tentando resolver nos próximos meses?"

### 7. Ferramentas

"Quais ferramentas você usa hoje? Cita as principais."

### 8. Identidade visual

"Sua marca tem identidade visual? Se tiver, pode me mandar o link do site, jogar uns prints em `marca/referencias/`, ou só descrever as cores e o estilo."

- **URL:** busque o site, analise cor dominante, tipografia e estilo, e confirme antes de escrever.
- **Imagens:** leia os arquivos de `marca/referencias/` e faça o mesmo.
- **Descrição em texto:** use direto.
- **Não tem:** diga que o sistema já vem com um guia em preto e branco que funciona, e que ele preenche quando tiver. Sem drama.

Depois, sempre: "Tem o logo em PNG ou SVG? Joga em `marca/logos/` e me diz o nome do arquivo. Se tiver versão pra fundo claro e escuro, manda as duas."

### 9. Escrita

"Como você quer que eu escreva? E o que mais te incomoda em texto feito por IA?"

### 10. Equipe

"Tem equipe ou é você que toca tudo?"

### 11. Números (opcional, mas vale muito)

"Última: quer já deixar seus clientes e valores cadastrados? Assim o painel de KPIs nasce funcionando. Se preferir depois, sem problema."

Se ele topar, pergunte cliente por cliente (nome, valor, se é mensal ou projeto) e depois preencha `financeiro/clientes-fees.md` e cadastre no painel:

```bash
cd .claude/skills/dash-kpis/scripts
python3 cli.py config negocio "[empresa]"
python3 cli.py config meta_recorrente [valor]
python3 cli.py cliente "[nome]" --valor [valor]
```

---

## O que gerar

Gere tudo de uma vez no fim, não a cada resposta.

### 1. `AGENTS.md`

O `AGENTS.md` é a fonte das instruções (o Claude Code lê via `CLAUDE.md → @AGENTS.md`, o Codex lê direto). Substitua o conteúdo genérico pelo do usuário, **mantendo a estrutura de seções que já está lá**: o bloco de contexto do negócio, as regras do sistema, o fluxo de trabalho, aprender com correções, manter contexto atualizado e criação de skills.

O que muda:

- Título: `# [Nome da Empresa]`
- "Sobre o negócio": o que a empresa faz, pra quem, tamanho do time
- "Estrutura de pastas": a lista real depois dos ajustes que você fizer no passo 5
- "Tom de voz": resumo de duas linhas, com o detalhe em `_contexto/preferencias.md`
- "Ferramentas conectadas": o que ele citou, marcando o que virou MCP

**Nunca escreva conteúdo no `CLAUDE.md`.** Ele tem uma linha só: `@AGENTS.md`. Se estiver diferente, corrija.

### 2. `_contexto/empresa.md`

```markdown
# Contexto da empresa

**Nome:** [pessoa]
**Empresa:** [empresa]
**O que faz:** [uma ou duas frases]
**Atende clientes:** [sim / não / os dois]
**Equipe:** [solo, ou quem faz o quê]
**Ferramentas:** [lista]
**Principais entregas:** [o que mais produz]

## Contexto adicional
[o que surgiu nas respostas e vale lembrar]
```

### 3. `_contexto/estrategia.md`

Fase do negócio, prioridade principal, o que pode esperar, e datas mencionadas.

### 4. `_contexto/preferencias.md`

Tom de voz, o que evitar (liste as palavras e construções que ele citou, literalmente), estilo geral, preferências adicionais.

### 5. `_contexto/agora.md`

Substitua o placeholder por este estado inicial, pra que o primeiro `/iniciar` já mostre alguma coisa:

```markdown
# Agora — contexto vivo

> Este é o contexto que muda toda semana (diferente de `estrategia.md`, que é o foco de fundo).
> O `/iniciar` lê isto no começo da sessão; o `/atualizar` escreve aqui no fim.

## Onde paramos
Configurei o sistema com o /setup. Próximo passo: rodar /mapear pra criar skills do meu dia a dia.

## Decisões recentes

## Pendências
- Rodar /mapear pra criar as primeiras skills.

## Quente agora
```

Não invente mais nada aqui. Este arquivo se preenche com o uso.

### 6. `marca/design-guide.md`

Se ele descreveu cores e estilo, substitua os valores do bloco `:root` e as seções de cor e tipografia. Se não tem identidade, deixe o preto e branco como está e diga que funciona. Mantenha o aviso do topo do arquivo.

Se ele deu o logo, preencha a seção **Logo** com o caminho real.

### 7. Adaptar as pastas

O sistema já vem com a estrutura montada. Seu trabalho aqui é **ajustar**, não criar do zero.

**Renomeie as duas pastas de conteúdo** (isso é obrigatório, e explique em uma linha por que):

```bash
mv conteudo/founder "conteudo/[primeiro-nome-da-pessoa]"
mv conteudo/empresa "conteudo/[nome-da-empresa-em-minusculo-com-hifen]"
```

Use `mv` puro, nunca `git mv`: na instalação por zip a pasta ainda não é um repositório git, e o `git mv` falha. Nomes em minúsculo, sem acento e com hífen no lugar de espaço.

> "Separei sua produção em duas: o que sai no seu nome e o que sai no nome da empresa. São públicos e tons diferentes, e misturar os dois é o erro mais comum."

**Depois pergunte o que não serve:**

> "A estrutura que veio é essa: [liste as pastas]. Tem alguma que não faz sentido pro seu negócio? Eu removo agora pra não ficar pasta vazia te olhando."

Remova o que ele disser. Se ele precisar de pasta que não existe (`obras/`, `producao/`, `estoque/`), crie e registre no `AGENTS.md`. Não force a estrutura padrão em quem tem operação diferente.

### 8. Conectores (MCPs)

Leia `templates/ferramentas/catalogo.md` e cruze com as ferramentas da pergunta 7. Pra cada uma que tiver conector, mostre o que ele faz e pergunte se quer instalar agora.

Se ele preferir depois, anote em `tarefas.md`:

```
- [ ] Instalar conector do [ferramenta] · `[comando]`
```

Se a ferramenta não estiver no catálogo, diga que não tem conector pronto e siga. Não invente comando de instalação.

---

## Mensagem final

> "[Nome], o sistema está configurado.
>
> - `AGENTS.md` — agora eu sei quem você é, o que a empresa faz e onde cada coisa mora
> - `_contexto/` — negócio, preferências e foco salvos
> - `marca/design-guide.md` — [preenchido com sua identidade / em preto e branco, pronto pra você preencher]
> - Pastas ajustadas pro seu negócio
> - [N] conectores instalados, [N] anotados pra depois
>
> **Duas coisas antes de continuar:**
>
> 1. Chave de API (se você tiver alguma) vai sempre num arquivo `.env`. Ele já está protegido e nunca sobe pro GitHub.
> 2. Pra não perder trabalho, conecte esta pasta ao GitHub com `/syncar`. Leva 2 minutos, e depois é só dizer "synca".
>
> **Próximo passo:** rode `/mapear`. Eu te entrevisto sobre o que você repete toda semana e crio as skills pra isso."

---

## Se o setup for interrompido no meio

Acontece: a pessoa para pra testar outra coisa, o computador fecha, ela volta amanhã. Duas regras pra isso não virar sistema meio configurado:

1. **Nunca escreva no arquivo um comentário sobre o processo.** Nada de `[setup não chegou nessa pergunta]`, `[a definir no setup]` ou parecido. Campo que você não perguntou fica **vazio**. Arquivo de contexto é lido em toda sessão: recado de processo lá dentro vira ruído permanente.
2. **Antes de parar, escreva o `AGENTS.md` com o que você já sabe.** Ele é o arquivo carregado em toda conversa; deixá-lo com os placeholders genéricos enquanto o `_contexto/` já está preenchido faz o sistema se comportar como se nunca tivesse sido configurado. Nome da empresa e o que ela faz já bastam pra valer a pena.

Ao retomar, releia `_contexto/` e `agora.md`, diga em uma linha o que já foi respondido e continue da pergunta seguinte. Não recomece do zero.

## Regras

- Tom direto e humano, sem entusiasmo de vendedor
- Uma pergunta por vez, em conversa. Nunca liste as dez de uma vez
- Resposta vaga pede uma pergunta de acompanhamento antes de seguir
- Gere os arquivos todos no fim, de uma vez
- Não liste cada linha de cada arquivo gerado. Resuma
- **Não invente dado do negócio.** Se a pessoa deu resposta que se contradiz (vende B2C mas cadastrou cliente mensal), pergunte em vez de escrever as duas versões no arquivo
- Se o usuário quiser pular uma pergunta, pule. Setup incompleto funciona; setup abandonado no meio, não
