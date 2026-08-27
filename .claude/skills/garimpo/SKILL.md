---
name: garimpo
description: >
  Garimpa conteúdo do Instagram pra virar matéria-prima de produção. Função 1 — baixa o perfil
  inteiro de um @ e separa em carrosseis, reels e estáticos, extraindo print de cada reel (1
  frame a cada 0,5s). Função 2 — recebe uma pasta com vídeos e devolve print, transcrição (por
  Whisper, rodando local) e 3 opções de headline por vídeo, no seu tom de voz.
  Use quando o usuário chamar /garimpo, ou disser "garimpa o @perfil", "baixa o instagram do
  fulano", "pega as referências desse perfil", "quero as capas dos reels", "capa de reels",
  "extrai print desse vídeo", "transcreve esses reels", "o que esse concorrente está postando",
  "headline pra esses vídeos", "analisa o perfil do concorrente", "banco de referência",
  ou colar um @ de Instagram pedindo material.
---

# /garimpo — o Instagram vira matéria-prima

## Pra que serve

Duas coisas que todo mundo faz na mão e leva horas:

1. **Baixar um perfil inteiro** e ter tudo separado por formato, com os frames dos reels já extraídos. Serve pra estudar concorrente, montar banco de referência, arquivar o próprio conteúdo ou entender o que um cliente novo vinha publicando.
2. **Transformar uma pasta de vídeos** em print + transcrição + headline. Serve pra escolher capa de reel, reaproveitar o que você já falou em vídeo como texto, e achar o trecho forte de uma gravação longa.

Tudo roda **na sua máquina**. Vídeo não sobe pra lugar nenhum, transcrição é local.

## Antes da primeira vez

Roda no Mac e no Linux. No Windows, use o WSL (Ubuntu) — os scripts são bash.

```bash
cd .claude/skills/garimpo
./verificar-deps.sh
```

Ele lista o que falta e o comando de cada um. As ferramentas:

| Ferramenta | Pra quê | Como instalar |
|---|---|---|
| gallery-dl | baixar do Instagram | `pip3 install --user --upgrade gallery-dl` |
| yt-dlp | reserva de download | `pip3 install --user --upgrade yt-dlp` |
| openai-whisper | transcrever (local) | `pip3 install --user --upgrade openai-whisper` |
| ffmpeg | extrair frames e juntar áudio | `brew install ffmpeg` (Linux: `sudo apt install ffmpeg`) |
| Firefox | onde fica a sessão logada do Instagram | `brew install --cask firefox` |

Se faltar alguma, mostre a lista pro usuário e pergunte se pode instalar antes de seguir.

## Função 1 — baixar um perfil

### 1. Coletar

- **@ do perfil** (obrigatório)
- **Nome da pasta** (opcional, o padrão é o próprio @)
- **Limite de posts** (opcional; sem limite baixa tudo, e perfil grande demora)

### 2. Checar a sessão

```bash
./checar-cookies.sh
```

- `OK` → seguir
- `FALTA_LOGIN` ou `FALTA_PROFILE` → peça pro usuário abrir o Firefox, entrar em instagram.com e logar. **Recomende uma conta secundária**, não a principal: download em volume pode chamar atenção do Instagram.

### 3. Baixar

```bash
./baixar-perfil.sh @usuario "nome-da-pasta" 30
```

Sai em `dados/garimpo/<pasta>/`:

```
<pasta>/
├── carrosseis/<post>/       01.jpg, 02.jpg...
├── reels/<post>/
│   ├── 01.mp4
│   └── prints/              frames a cada 0,5s
└── estaticos/<post>.jpg
```

### 4. Reportar

Quantos reels, carrosséis e estáticos, quantos prints e o caminho. Se o usuário pediu pra estudar o perfil, **não pare no inventário**: olhe os prints e as legendas e devolva o que dá pra ver (formato dominante, padrão de gancho, tema que ele repete, o que ele nunca fala).

## Função 2 — capa e transcrição de uma pasta de vídeos

### 1. Rodar

```bash
./extrair-capas.sh "/caminho/da/pasta" pt
```

Idioma: `pt` (padrão), `en`, `es`, ou `auto`. Cria dentro da pasta: `prints/`, `transcricoes/` e `headlines/`.

### 2. Gerar as headlines — **esta parte é sua, não do script**

1. Leia cada `.txt` de `transcricoes/`
2. Leia `_contexto/preferencias.md` pra pegar o tom de voz do usuário
3. Pra cada vídeo, escreva **3 headlines** e salve em `headlines/<video>.md`
4. **Mostre as três no chat**, sempre. Não mande o usuário abrir arquivo

Regras de headline de capa:

- **Máximo 6 palavras**, idealmente 3 a 5. Headline longa não vira capa boa
- Idioma igual ao da transcrição
- Varie os três ângulos: **(a)** número ou fato concreto, **(b)** afirmação seca, **(c)** gancho de identificação

Formato do arquivo:

```markdown
# Headlines — <nome do vídeo>

**Tema:** <uma linha>
**Trecho-chave:** "<a frase mais forte da transcrição>"

## Opções

1. <headline>
2. <headline>
3. <headline>
```

## O que costuma dar errado

- **Firefox com a sessão expirada.** Erro 401 ou 403: peça pro usuário relogar.
- **`database is locked`.** O Firefox está segurando os cookies. Feche-o e rode de novo (`osascript -e 'tell application "Firefox" to quit'` no Mac).
- **Vídeo e áudio separados** (`*v.mp4` + `*a.m4a`): o ffmpeg não estava acessível na hora do download. Rode `./mergear.sh <pasta>`.
- **A primeira transcrição demora**: o Whisper baixa o modelo `small` (~460 MB) uma vez e guarda em cache. Depois, conte cerca de 5x a duração do vídeo em processamento.
- **`.txt` vazio não é erro.** É reel instrumental, sem fala. Não gere headline pra esses.
- **Perfil privado não baixa**, mesmo logado, se a conta do Firefox não seguir o perfil.

## Regras

- **Referência é estudo, não cópia.** Ao devolver análise de concorrente, aponte o padrão e o que fazer diferente, nunca ofereça reproduzir o post dele.
- **Peça o limite em perfil grande.** 500 posts levam muito tempo e aumentam o risco de bloqueio. Comece com 30.
- **Nunca suba o material baixado pro git.** `dados/garimpo/` já está no `.gitignore`.
- Conteúdo de terceiro baixado é material de consulta interna. Republicar exige autorização de quem publicou.

## Arquivos

- [verificar-deps.sh](verificar-deps.sh) — checa as ferramentas
- [checar-cookies.sh](checar-cookies.sh) — valida a sessão do Instagram no Firefox
- [baixar-perfil.sh](baixar-perfil.sh) — Função 1
- [organizar.py](organizar.py) — separa em carrosseis, reels e estáticos e extrai os prints
- [extrair-capas.sh](extrair-capas.sh) — Função 2
- [mergear.sh](mergear.sh) — junta vídeo e áudio órfãos
