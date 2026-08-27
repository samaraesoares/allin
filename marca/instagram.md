# Padrão de Instagram — Samara Soares / All In

> Especificação para carrossel, lâmina e story. Toda skill que gerar peça de Instagram lê este arquivo **junto com** `design-guide.md`.
> **Referências visuais:** `marca/referencias/instagram/ref-01` a `ref-15`
> **Definido em:** 2026-08-26 · a partir das 15 peças enviadas pela Samara

---

## O diagnóstico

Nas 15 peças analisadas existem **três sistemas visuais diferentes** rodando ao mesmo tempo, mais variações de rodapé. Isso divide o reconhecimento: o feed não parece de uma marca só.

A padronização abaixo escolhe **um sistema principal** e dá função específica aos outros dois, em vez de eliminá-los.

---

## SISTEMA 1 — CARROSSEL *(o principal)*

**Formato:** 1080 × 1350 (4:5)
**Quando:** todo carrossel de conteúdo. É o padrão.
**Referências:** `ref-06`, `ref-08`, `ref-11`, `ref-12`

Foto vertical ocupando a peça inteira, **sem escurecimento global**, com caixas de texto sólidas empilhadas sobre ela.

### As três caixas

A cor da caixa não é decoração — ela marca a função da frase na narrativa:

| Caixa | Fundo | Texto | Função |
|---|---|---|---|
| **Preta** | `#0D0D0D` | off-white `#FFFCF9` | o setup — a pergunta, o contexto, a afirmação comum |
| **Dourada** | `#C9A47A` | off-white `#FFFCF9` | a virada — a consequência, o erro, o que dói |
| **Branca** | `#FFFCF9` | navy `#091422` | a resolução — o que fazer, a definição, a prova |

**Regra de sequência:** no máximo **três caixas por lâmina**, sempre em ordem narrativa (setup → virada → resolução). Nunca duas caixas da mesma cor coladas.

### Especificação

- **Tipografia da caixa:** serif (Kepler Std Display, fallback Bodoni Moda), peso 400–600, **caixa de sentença** — não uppercase
- **Ênfase dentro da frase:** a palavra-chave em UPPERCASE (`PREÇO`, `VALOR`, `ETAPAS`)
- **Alinhamento:** centralizado
- **Largura da caixa:** ajusta ao texto, nunca sangra a borda — margem lateral mínima de 80px
- **Padding interno:** 28px vertical · 40px horizontal
- **Espaço entre caixas:** 16px
- **Border-radius:** 0 — as caixas são retangulares
- **Posição do bloco:** ancorado na metade inferior, entre 50% e 80% da altura

### Contador de slides

Canto superior direito, `24px` da borda. Formato `1/6`. SF Pro Display, 400, 28px, off-white. Sempre presente em carrossel.

### Rodapé (obrigatório em toda lâmina)

Barra sólida **navy `#091422`**, altura 88px, colada na base.

Texto centralizado: `All In  •  Pitch Imparável®  •  @samaraesoares`

- SF Pro Display Light 300, 26px, off-white `#FFFCF9`
- Separadores `•` em dourado `#C9A47A`
- Letter-spacing `0.06em`
- **O `®` é obrigatório.** Pitch Imparável é marca registrada — sem ele em algumas peças e com ele em outras, enfraquece a marca

---

## SISTEMA 2 — LÂMINA SPLIT *(peça de declaração)*

**Formato:** 1080 × 1080 (1:1)
**Quando:** post único de frase forte, quote ou posicionamento. **Não** usar em carrossel.
**Referências:** `ref-01`, `ref-02`, `ref-03`

Duas fotos empilhadas, metade e metade, **ambas escurecidas** (overlay navy `#091422` a 55%).

### Especificação

**Metade de cima — a declaração:**
- Serif (Kepler Std Display, fallback Bodoni Moda), 400–600
- Off-white `#FFFCF9`, centralizado, ~86px
- Caixa de sentença, ponto final incluso
- Abaixo dela: **o divisor dourado** — linha de 1px em `#C9A47A` a 60% de opacidade, largura ~55% da peça, com um losango de 4 pontas em `#C9A47A` no centro

**Metade de baixo — o desdobramento:**
- SF Pro Display Light 300, off-white, centralizado, ~44px
- Duas linhas no máximo
- Continua a frase de cima — não repete, não resume

**Rodapé:** idêntico ao Sistema 1.

**Variação aceita:** trocar o losango por uma barra dourada curta (`ref-02`) quando a frase de cima for curta.

---

## SISTEMA 3 — STORY *(texto puro)*

**Formato:** 1080 × 1920 (9:16)
**Quando:** story de reflexão, quote, resposta a pergunta. Sem foto.
**Referência:** `ref-15`

- **Fundo:** off-white `#FFFCF9`
- **Citação/pergunta:** SF Pro Display 300, navy `#091422`, com **barra vertical dourada** `#C9A47A` de 6px à esquerda, 24px de respiro
- **A resposta comum:** SF Pro Display 300, navy
- **O punch:** **Kepler Std Italic Bold 700, UPPERCASE**, navy — aqui a regra do manual vale integralmente
- **Rodapé:** `ALL IN  •  @samaraesoares`, SF Pro Display 300, UPPERCASE, tracking `0.20em`, cinza `rgba(9,20,34,0.35)`, centralizado

---

## Regra da tipografia — como resolver o conflito com o manual

O manual de marca diz **"Kepler Std é sempre UPPERCASE"**. As peças de Instagram usam serif em caixa de sentença. As duas coisas convivem assim:

| Uso | Caixa |
|---|---|
| **Punch / display / hero** — capa, CTA, frase-assinatura, story | **UPPERCASE**, italic bold — regra do manual |
| **Corpo do carrossel e da lâmina** — caixas de texto, declaração split | **Caixa de sentença**, romano |
| **Palavra-chave dentro da frase** | **UPPERCASE**, mesmo tamanho |

Assim a textura uppercase italic continua sendo assinatura, sem virar ruído em bloco de texto longo.

---

## Foto

- **Sempre foto real da Samara.** Nunca banco de imagem.
- Nunca alterar rosto, corpo ou cor da pele.
- No Sistema 1 a foto entra sem escurecimento — as caixas garantem a leitura.
- No Sistema 2 as duas fotos são escurecidas por igual.
- Foto de evento, palco e bastidor tem prioridade sobre foto posada.

---

## O que NUNCA fazer

- Misturar Sistema 1 e Sistema 2 dentro do mesmo carrossel
- Mais de três caixas de texto numa lâmina
- Duas caixas da mesma cor coladas
- Rodapé sem o `®` de Pitch Imparável®
- Rodapé com hífen (`-`) no lugar do bullet (`•`)
- Barra de rodapé preta — é navy `#091422`
- Texto sangrando na borda
- Caixa de texto com canto arredondado
- Terceira cor de caixa além de preto, dourado e branco

---

## Status

✅ **Aprovado pela Samara em 2026-08-26.** Este é o padrão. Toda peça de Instagram sai daqui.

As três decisões aprovadas:
1. **Formato principal:** 4:5 (1080×1350) — ocupa mais área no feed que 1:1 e as caixas seguram a leitura mesmo em foto de celular com luz ruim
2. **Rodapé:** barra navy `#091422` com bullets dourados e o `®` obrigatório
3. **Uppercase:** reservado pro punch (capa, CTA, story, palavra-chave). Corpo de carrossel em caixa de sentença

**Nota:** `ref-04` é print do perfil `@eusounarav` — referência externa, não peça da Samara. Mantido só como inspiração do formato split.
