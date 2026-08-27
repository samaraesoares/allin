# Beza OS

O sistema operacional do seu negócio dentro do Claude Code. Uma pasta que lembra quem você é, o que você vende, quem são seus clientes, quanto entra e quanto sai, e que executa o trabalho repetitivo com você.

São três passos. Uns 20 minutos, contando a instalação.

---

## 1. Instale o Claude Code

Você precisa de uma **conta paga da Anthropic** (claude.ai) e de um computador. Só isso.

**No Mac**

Abra o **Terminal** (aperte `Cmd + Espaço`, digite "Terminal", Enter) e cole:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**No Windows**

Abra o **PowerShell** (aperte a tecla Windows, digite "PowerShell", Enter) e cole:

```powershell
irm https://claude.ai/install.ps1 | iex
```

Feche e abra o terminal de novo quando terminar.

---

## 2. Abra esta pasta

Descompacte o arquivo `beza-os.zip` onde você quiser guardar (sugestão: a pasta Documentos).

Depois, no mesmo terminal, entre na pasta e chame o Claude:

**Mac**
```bash
cd ~/Documents/beza-os
claude
```

**Windows**
```powershell
cd $HOME\Documents\beza-os
claude
```

Na primeira vez ele vai pedir pra você entrar com a sua conta. Uma janela do navegador abre, você aprova, e volta pro terminal.

---

## 3. Rode o setup

Com o Claude aberto, digite:

```
/setup
```

Ele vai te fazer algumas perguntas sobre o seu negócio (nome, o que você vende, como você escreve, quais ferramentas usa) e configurar tudo sozinho. Responda com calma: quanto mais específico, melhor o sistema trabalha pra você.

**Pronto. O sistema é seu.**

---

## O que fazer depois

| Comando | O que acontece |
|---|---|
| `/mapear` | ele te entrevista sobre o que você repete toda semana e cria comandos sob medida pra isso |
| `/iniciar` | comece toda sessão por aqui: ele carrega o contexto e mostra onde você parou |
| `/dash-kpis` | seu painel de números: receita, clientes, funil e meta |
| `/agenda-tarefas` | o plano do dia e da semana, em cima da sua lista de tarefas |
| `/fechamento-mes` | fecha o mês e guarda o histórico |
| `/fluxo-caixa` | mostra quando o caixa aperta nos próximos 90 dias |
| `/garimpo` | baixa o Instagram de um perfil e vira print, transcrição e headline |
| `/syncar` | salva tudo no GitHub, pra você nunca perder o trabalho |

Você também pode simplesmente **conversar**. "Monta uma proposta pro João", "vira essa reunião em ata", "quanto eu tenho de recorrente?", "escreve um post sobre isso". O sistema já sabe do seu negócio.

---

## Se travar

- **`claude` não é reconhecido:** feche o terminal e abra de novo. Se persistir, refaça o passo 1.
- **Ele pede permissão o tempo todo:** normal no começo. Aceite as que fizerem sentido; ele aprende.
- **Perdeu a janela:** é só abrir o terminal, entrar na pasta de novo (`cd`) e digitar `claude`.
- **Qualquer outra dúvida:** pergunte pro próprio Claude, dentro da pasta. Ele conhece este sistema.
