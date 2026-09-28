# Diagnóstico Pitch Imparável®

Quiz de diagnóstico de vendas no formato "responde → deixa o contato → recebe o resultado".
É um lead magnet: leva o lead até a **Sessão de Diagnóstico** (`form.respondi.app/x7aEH3jt`).

**Criado em:** 2026-09-28

## Como funciona

1. **Intro:** gancho da Síndrome do Evento Bonito™ + foto de palco
2. **12 perguntas:** 3 por bloqueio (Produto sem Desejo™, Comunicação sem Influência™, Evento sem Jornada™, Comercial sem Continuidade™). Cada resposta vale de 0 a 3. A ordem das opções é embaralhada
3. **Captura:** nome, WhatsApp, e-mail, Instagram, atuação, faturamento, equipe comercial
4. **Resultado:** Índice de Conversão (0–100), nível, % de cada bloqueio, bloqueio principal (o menor %), pilar de entrada e o CTA pra aplicação

| Índice | Nível |
|---|---|
| 0–39 | Venda no improviso |
| 40–69 | Conversão que depende de você |
| 70–100 | Pronto pra escalar |

**Indicação interna** (vai só pro webhook, o lead não vê): PERFORMANCE se fatura R$ 50k+ e tem equipe · SPRINT se o bloqueio principal é Produto sem Desejo™ · senão NÚCLEO / ESTRATÉGIA. É hipótese pra Samara ler antes da call, não decisão.

## O que falta pra ir ao ar

Tudo se configura no bloco `CONFIG` no topo do `<script>` do `index.html`.

1. **Salvar os leads** (hoje não salva em lugar nenhum). Caminho mais simples, Google Sheets:
   - Criar uma planilha → Extensões → Apps Script → colar:
     ```js
     function doPost(e) {
       const d = JSON.parse(e.postData.contents);
       const sh = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
       if (sh.getLastRow() === 0) sh.appendRow(Object.keys(d));
       sh.appendRow(Object.keys(d).map(k => d[k]));
       return ContentService.createTextOutput('ok');
     }
     ```
   - Implantar → Nova implantação → App da Web → acesso "Qualquer pessoa" → copiar a URL pra `CONFIG.webhook`
   - Alternativa: webhook do Zapier/Make pra mandar o lead direto pro WhatsApp ou CRM
2. **Meta Pixel** (opcional): colocar o ID em `CONFIG.pixelId`. Dispara PageView, Lead e ViewContent
3. **Hospedar:** subir a pasta inteira (`index.html` + `samara-palco.jpg`) no Vercel ou Netlify (arrasta a pasta, sai com link). Depois apontar um subdomínio, ex. `diagnostico.samarasoares.com`
4. **Fontes:** a página usa Kepler Std se estiver instalada; senão cai no Bodoni Moda (Google Fonts). Pra Kepler aparecer pra todo mundo, subir o `.woff2` junto e declarar um `@font-face`

## Pra mexer no conteúdo

Perguntas, textos dos bloqueios e níveis ficam em `QUESTIONS`, `BLOCKS` e `LEVELS`, no `<script>`. Os nomes ™ vêm de `comercial/metodo-pitch-imparavel.md` e não devem ser parafraseados.
