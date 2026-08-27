---
name: carrossel
description: >
  Cria carrossel, lâmina e story de Instagram no padrão aprovado da Samara Soares / All In.
  Escreve o texto no tom dela, monta o HTML com a identidade da marca e renderiza em PNG
  via Playwright, usando as fotos reais do banco em marca/fotos/.
  Use quando a Samara disser "carrossel", "lâmina", "faz um post", "slide pro Instagram",
  "story", "transforma isso em carrossel", "post sobre X", ou colar um texto pedindo pra virar peça.
---

# /carrossel — peça de Instagram no padrão All In

## Antes de tudo, ler

1. `marca/instagram.md` — **a especificação.** Os três sistemas, as caixas, o rodapé, as regras.
2. `marca/design-guide.md` — paleta e tipografia
3. `_contexto/preferencias.md` — tom de voz e o que evitar
4. `comercial/metodo-pitch-imparavel.md` — os mecanismos ™ e os 4 pilares, quando o tema for método

Não perguntar cor, fonte nem estilo. **Já está tudo definido e aprovado.** Perguntar de novo é erro.

---

## Passo 1 — Escolher o sistema

| O que a Samara pediu | Sistema | Formato |
|---|---|---|
| carrossel, slides, sequência, "post sobre X" | **1 — Carrossel** | 1080×1350 |
| frase forte, quote, posicionamento, peça única | **2 — Lâmina split** | 1080×1080 |
| story, enquete, reflexão rápida | **3 — Story** | 1080×1920 |

Na dúvida, Sistema 1 — é o padrão.
**Nunca misturar Sistema 1 e 2 no mesmo carrossel.**

## Passo 2 — Escrever o texto primeiro

Texto antes de design. Peça bonita com texto fraco não converte.

**A estrutura narrativa do carrossel:**

| Lâmina | Função |
|---|---|
| 1 — capa | a promessa ou a dor. Para o scroll |
| 2 a N−1 — desenvolvimento | uma ideia por lâmina. Nunca duas |
| N — CTA | o próximo passo concreto |

**Regras de escrita** (de `_contexto/preferencias.md`):
- Direto, confiante, estratégico. Autoridade sem arrogância
- Frase curta. Uma ideia por lâmina
- Problema → transformação → prova → próximo passo
- **Evitar:** clichê sem profundidade, promessa vaga, frase bonita sem função comercial, lista de credencial tipo currículo, urgência artificial, "mega desconto"
- Nunca reduzir a Samara a "mentora de apresentação" — o escopo é método, oferta, posicionamento, processo comercial, pitch e venda

**Quando o tema for o método**, usar os nomes registrados, nunca a paráfrase: Síndrome do Evento Bonito™, Produto sem Desejo™, Comunicação sem Influência™, Evento sem Jornada™, Comercial sem Continuidade™, e os 4 pilares.

**Mostrar o texto pra Samara antes de renderizar.** Ela aprova ou ajusta, e só então vira imagem.

## Passo 3 — Escolher as fotos

Ler o que existe em `marca/fotos/` (`palco/`, `bastidor/`, `retrato/`, `lifestyle/`).

- **Prioridade:** palco > bastidor > retrato > lifestyle
- Uma foto por lâmina, sem repetir dentro do mesmo carrossel
- Escolher foto com **espaço vazio** onde a caixa de texto vai entrar, pra não cobrir o rosto
- **Nunca usar banco de imagem. Nunca alterar rosto, corpo ou cor da pele.**

**Se `marca/fotos/` estiver vazia:** avisar e oferecer as duas saídas — a Samara joga fotos na pasta agora, ou a peça sai em **fundo navy sólido `#091422`** sem foto. Não inventar foto, não usar stock.

## Passo 4 — Montar o HTML

Usar `template.html` desta pasta como base. Ele já traz os três sistemas em CSS, na especificação exata.

**Fonte:** o ideal é Kepler Std e SF Pro Display instaladas (`marca/fontes/`).
Enquanto não estiverem, o template cai pra **Bodoni Moda** (serif) e **Inter** (sans) do Google Fonts — fica ~90% do visual. Não travar por causa de fonte.

Um arquivo HTML por lâmina, em pasta temporária.

## Passo 5 — Renderizar em PNG

```bash
npx playwright screenshot --viewport-size=1080,1350 lamina-01.html lamina-01.png
```

Ajustar o viewport ao sistema: `1080,1350` (carrossel) · `1080,1080` (split) · `1080,1920` (story).

Se o Playwright não estiver instalado:
```bash
npx playwright install chromium
```

## Passo 6 — Salvar e entregar

Salvar em `conteudo/samara/carrosseis/AAAA-MM-DD-tema/`:

```
2026-08-27-sindrome-do-evento-bonito/
  lamina-01.png ... lamina-06.png
  legenda.md
  fonte.html/          ← os HTMLs, pra reeditar sem refazer
```

**Escrever também a legenda** em `legenda.md`: gancho na primeira linha (é o que aparece antes do "mais"), desenvolvimento curto, CTA, e 3 a 5 hashtags. Mesmo tom das lâminas.

Mostrar os PNGs pra Samara com `SendUserFile`.

---

## Checklist antes de entregar

- [ ] Rodapé em toda lâmina: barra navy `#091422`, `All In • Pitch Imparável® • @samaraesoares`
- [ ] O **`®`** está lá
- [ ] Bullets `•` dourados `#C9A47A` — nunca hífen
- [ ] Contador `1/6` no canto superior direito (só carrossel)
- [ ] Máximo 3 caixas por lâmina, em ordem narrativa: preta (setup) → dourada (virada) → branca (resolução)
- [ ] Nunca duas caixas da mesma cor coladas
- [ ] Caixas sem canto arredondado
- [ ] Nenhum texto sangrando na borda — margem lateral mínima 80px
- [ ] Corpo em caixa de sentença; UPPERCASE só no punch e na palavra-chave
- [ ] Foto real da Samara, sem alteração de rosto ou corpo

## O que nunca fazer

- Perguntar cor, fonte ou estilo — já está definido
- Misturar Sistema 1 e 2 no mesmo carrossel
- Usar banco de imagem
- Renderizar antes da Samara aprovar o texto
- Terceira cor de caixa além de preto, dourado e branco
