# Catálogo de skills prontas

Skills que já existem e você pode chamar sem criar nada. Use como referência quando o `/mapear` for procurar se já tem algo pronto antes de escrever uma skill do zero.

> Skill global fica em `~/.claude/skills/` e funciona em qualquer projeto.
> Skill local fica em `.claude/skills/` e só funciona nesta pasta.

---

## Já vêm no seu sistema

| Skill | O que faz |
|---|---|
| `/setup` | configura o sistema pro seu negócio |
| `/iniciar` | abre a sessão com o contexto carregado |
| `/mapear` | entrevista você e cria skills sob medida |
| `/atualizar` | corrige o contexto que ficou desatualizado |
| `/syncar` | salva tudo no GitHub |
| `/novo-projeto` | cria pasta de cliente ou projeto com contexto próprio |
| `/dash-kpis` | painel local com os números do negócio |
| `/agenda-tarefas` | plano do dia, captura e fechamento de tarefa |
| `/fechamento-mes` | fecha o mês e escreve o histórico |
| `/fluxo-caixa` | projeção de caixa de 90 dias |
| `/garimpo` | baixa perfil do Instagram e vira print, transcrição e headline |

---

## Nativas do Claude Code

Estas vêm com o próprio Claude Code. Não precisa instalar nada.

### Frontend Design
**O que faz:** cria interface web completa com HTML/CSS/React, com visual profissional.
**Bom pra:** landing page, painel, página de produto.
**Chamar com:** `/frontend-design`

### Canvas Design
**O que faz:** cria arte visual em PNG e PDF com princípios de design.
**Bom pra:** capa, banner, peça gráfica, thumbnail.
**Chamar com:** `/canvas-design`

### PDF
**O que faz:** extrai texto e tabela de PDF, cria, junta, separa e preenche formulário.
**Bom pra:** ler contrato, gerar relatório, extrair dado de nota.
**Chamar com:** `/pdf`

### DOCX
**O que faz:** cria e edita documento Word com formatação e comentários.
**Bom pra:** contrato, documento pra cliente que pede Word.
**Chamar com:** `/docx`

### PPTX
**O que faz:** cria e edita apresentação PowerPoint.
**Bom pra:** quando o cliente exige o arquivo em PowerPoint. Pro seu material, o modelo em `apresentacoes/_modelo/` costuma ficar melhor.
**Chamar com:** `/pptx`

### XLSX
**O que faz:** cria e edita planilha com fórmula, formatação e gráfico.
**Bom pra:** relatório, análise de dado, planilha pro contador.
**Chamar com:** `/xlsx`

### Doc Co-Authoring
**O que faz:** fluxo guiado pra escrever documento a quatro mãos: entrevista, rascunho, validação.
**Bom pra:** proposta técnica, procedimento interno, documento de decisão.
**Chamar com:** `/doc-coauthoring`

### Webapp Testing
**O que faz:** testa site local com navegador de verdade, tira print e lê erro de console.
**Bom pra:** conferir uma landing antes de publicar.
**Chamar com:** `/webapp-testing`

### Find Skills
**O que faz:** procura skill pronta pra um problema que você descreve.
**Bom pra:** quando o `/mapear` não achou template e você quer pesquisar antes de criar.
**Chamar com:** `/find-skills`

### Skill Creator
**O que faz:** guia pra criar skill nova do zero, com a estrutura certa.
**Bom pra:** skill mais complexa, que o `/mapear` sozinho não cobre.
**Chamar com:** `/skill-creator`

---

## Conectores úteis

### Context7
**O que faz:** busca documentação atualizada de biblioteca e framework, pro Claude não usar informação velha.
**Bom pra:** qualquer skill que envolva código.
**Instalar:** `claude mcp add context7 -- npx -y @upstash/context7-mcp`

Mais conectores (Notion, Drive, Gmail, Agenda, redes sociais, anúncios) estão em `templates/ferramentas/catalogo.md`.

---

## Como adicionar skill nova neste catálogo

Testou uma skill e quer registrar pra lembrar depois:

```markdown
### Nome da skill
**O que faz:** [uma frase]
**Bom pra:** [caso de uso prático]
**Instalar:** [comando ou "nativa"]
```
