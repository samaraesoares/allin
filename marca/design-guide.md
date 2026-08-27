# Guia de Design — Samara Soares

> **Fonte:** Manual de Identidade Visual — https://samara-visual.vercel.app/ · cópia local em `marca/referencias/manual-de-marca.html`
> **Produção:** Beza Media · 2026
> **Atualizado em:** 2026-08-26
>
> Toda skill que gera visual (apresentação, proposta, carrossel, slide, landing) lê este arquivo antes de criar qualquer coisa.

**Posicionamento da marca:**
> Estrategista de vendas, liderança e legado.
> Uma marca que confronta a mediocridade e ativa propósitos.

**Pilares:** Negócios · Liderança · Fé
**Handle:** @samaraesoares

> **Peça de Instagram?** A especificação de carrossel, lâmina e story está em [`instagram.md`](instagram.md). Ler os dois.

---

## Princípios

**Escuridão com profundidade.** Tons de azul-marinho com o dourado como **único** acento. A paleta comunica autoridade, sofisticação e propósito.

1. **A marca é dark-first.** Navy é o fundo padrão, não a exceção. Material claro é a versão invertida, não o contrário.
2. **Um acento só: o dourado.** Ele marca palavra de impacto, CTA, número e etiqueta de seção. Nunca em bloco grande de fundo.
3. **Espaço em branco é elemento de design.** Muito respiro, hierarquia simples.
4. **Nada existe só pra ficar bonito.** Cada peça cumpre função na jornada: posicionamento, prova, conversa, aplicação ou venda.

---

## Cores

Os tokens abaixo são o que as skills leem. Troque os valores, mantenha os nomes.

```css
:root {
  --navy:          #091422;   /* fundo principal */
  --navy-mid:      #0E1F38;   /* fundo secundário, painéis */
  --navy-light:    #152A4A;   /* hover states, variações */
  --gold:          #C9A47A;   /* acento, destaques, CTA */
  --gold-soft:     #E2C9A4;   /* textos sobre navy escuro */
  --white:         #FFFFFF;   /* textos principais */
  --off-white:     #FFFCF9;   /* bege quente, textos suaves */
  --muted:         rgba(255,252,249,0.45);  /* texto secundário */
  --muted-strong:  rgba(255,252,249,0.70);  /* texto secundário forte */

  /* aliases pras skills que esperam nomes genéricos */
  --bg:            #091422;
  --bg-soft:       #0E1F38;
  --text:          #FFFCF9;
  --text-muted:    rgba(255,252,249,0.70);
  --accent:        #C9A47A;
  --accent-contra: #091422;
  --border:        rgba(201,164,122,0.10);
  --border-strong: rgba(201,164,122,0.30);
}
```

| Nome | Hex | Papel |
|---|---|---|
| **Navy** | `#091422` | fundo principal |
| **Navy Médio** | `#0E1F38` | fundo secundário, painéis |
| **Navy Light** | `#152A4A` | hover states, variações |
| **Gold** | `#C9A47A` | acento, destaques, CTA |
| **Gold Soft** | `#E2C9A4` | textos sobre navy escuro |
| **Branco** | `#FFFFFF` | textos principais |
| **Off-white** | `#FFFCF9` | bege quente, textos suaves |

**Versão clara** (quando o material precisar de fundo claro): fundo off-white `#FFFCF9`, texto navy `#091422`, dourado segue como acento.

**Cor proibida:** qualquer cor fora do par navy + dourado. Nada de neon, pastel, gradiente colorido ou segunda cor de acento.

---

## Tipografia

**Kepler Std + SF Pro Display.** SF Pro Display para leitura — neutra, técnica, com clareza. Kepler Std Italic Bold (Display) para as palavras que precisam ser lembradas.

### ⚠️ Regra inegociável

**Kepler Std é SEMPRE em UPPERCASE.** Nunca em caixa baixa ou title case. A textura serifada italic + caps é a assinatura visual da marca. Renderizar via CSS (`text-transform: uppercase`), não confiar na digitação.

### Os quatro papéis

| Papel | Fonte | Peso / Estilo | Caixa | Uso |
|---|---|---|---|---|
| **Display / Impacto** | Kepler Std (Display) | Italic Bold 700 | UPPERCASE — sempre | palavras de impacto, CTA display, títulos heroicos |
| **Corpo / Narrativo** | SF Pro Display | Light 300 · destaque SemiBold 600 | normal | full slides, texto narrativo, legendas |
| **Quote / Response** | SF Pro Display | Light 300 · destaque SemiBold 600 | UPPERCASE, centralizado | quotes do carrossel split |
| **Label / Assinatura** | SF Pro Display | Light 300 · tracking 0.20em–0.35em | UPPERCASE | rodapé CTA, handle, nome no header |

```css
font-family: 'Kepler Std', 'Bodoni Moda', serif;              /* display */
font-family: 'SF Pro Display', system-ui, -apple-system, sans-serif;  /* corpo */
```

**Fallbacks:** Kepler Std → Bodoni Moda → serif. SF Pro Display → system-ui.

### Escala nos slides (base 1080px)

| Tamanho | Exemplo |
|---|---|
| 130px | `IDENTIFICOU` — display máximo |
| 72px | `Se você se` — display secundário |
| 54px | texto narrativo no full slide |
| 44px | `DESTRAVAR` — display de apoio |
| 38px | `QUOTE / RESPONSE` |
| 17px | `SAMARA SOARES` — assinatura |

---

## Logo & Isologo

Três arquivos, todos SVG vetorial:

| Arquivo | Quando usar |
|---|---|
| `logo-lockup.svg` | lockup completo, sobre fundo escuro |
| `logo-lockup` invertido | sobre fundo claro (navy `#091422`) |
| `isologo.svg` | o símbolo isolado |
| `wordmark.svg` | a assinatura em texto |

**Regras:**
- **O isologo é o único elemento de marca nos slides.** Nunca duplicar com o wordmark.
- **Posicionamento nos slides:** o isologo aparece **apenas no slide CTA (slide 8)**, em `top: 220px`, centralizado.
- Nos demais slides: **sem marca** — só avatar circular + `@handle` no header.
- Área de respiro: nunca encostar nada a menos da altura do logo em volta dele.

**Arquivos no sistema:**

| Arquivo | Status |
|---|---|
| `marca/logos/wordmark.svg` | ✅ salvo — 648×37, `fill="#FFFCF9"` (off-white, pra fundo escuro) |
| `logo-lockup.svg` | ⬜ pendente |
| `isologo.svg` | ⬜ pendente |
| versão invertida (navy) | ⬜ pendente |

**Fonte dos arquivos:** Google Drive → `Fontes e Logo` → pasta `Logo`
https://drive.google.com/drive/folders/1mkE_AU1UR_z8WUCK7TgfN5qH2pS0g589

---

## Arquivos de fonte

As fontes não são de sistema — precisam ser instaladas pro material renderizar certo.

| Fonte | Onde está |
|---|---|
| **Kepler Std** (Display: Regular, Italic, Semibold, Semibold It, Bold, Bold It) | Drive → `kepler-std-3-cdnfonts` |
| **SF Pro Display** (Regular, Medium, Bold) | Drive → `sf-pro-display` |

**Pendente:** copiar os `.otf` pra `marca/fontes/` e instalar no Windows. Sem eles, o HTML cai no fallback (Bodoni Moda / system-ui) e a assinatura visual se perde.

---

## Estilo geral

Editorial, escuro e premium. Muito respiro, borda de 1px em dourado a 10% de opacidade, zero sombra pesada, zero gradiente decorativo colorido. Gradiente radial sutil de dourado (7% de opacidade) é aceito como textura de fundo em hero.

**Elementos-chave:**
- **Bordas:** 1px em `rgba(201,164,122,0.10)`
- **Border-radius:** 12px em card, 8px em botão, 0 em imagem de capa
- **Botões:** fundo `--gold`, texto `--navy`
- **Etiqueta de seção:** SF Pro Display, 11px, UPPERCASE, tracking 0.18em, cor `--gold`
- **Easing de animação:** `cubic-bezier(0.16, 1, 0.3, 1)`

---

## Foto

- **Foto original permanece colorida e fiel à imagem real da Samara.** Nunca alterar rosto ou corpo.
- Imagem em tela inteira funciona bem; escurecer levemente quando precisar acomodar texto com contraste.
- Texto sobre foto sempre com faixa ou escurecimento por trás.

---

## O que NUNCA fazer

- **Kepler Std em caixa baixa ou title case** — é a regra inegociável da marca
- Duplicar isologo e wordmark na mesma peça
- Colocar marca em slide que não seja o CTA
- Mais de duas famílias tipográficas no mesmo material
- Texto em cima de foto sem faixa ou escurecimento por trás
- Alterar rosto, corpo ou cor real da Samara em foto
- Dourado em bloco grande de fundo (ele é acento, não fundo)
- Segunda cor de acento
- Poluição visual, excesso de elemento, peça que não conduz a nada

---

## Perfil do autor

> Usado quando o material sai no nome da pessoa (post, carrossel estilo tweet, assinatura de proposta).

- **Nome:** Samara Soares
- **Handle:** @samaraesoares
- **Assinatura padrão:** `SAMARA SOARES  ·  @samaraesoares` (SF Pro Display Light 300, UPPERCASE, tracking 0.20em)
- **Foto:** *(colocar em `marca/logos/foto-perfil.jpg`)*

---

## A confirmar

Este manual é da **marca pessoal Samara Soares** (@samaraesoares). As propostas comerciais em PDF da **ALL IN / Pitch Imparável®** parecem seguir um tratamento diferente. Confirmar: a All In usa esta mesma identidade, ou tem manual próprio?

## Observações adicionais
