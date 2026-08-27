# propostas/_modelo/

`proposta.html` é o modelo comercial do sistema. Mesma lógica do deck: preto e branco, tokens de `marca/design-guide.md`, abre no navegador, vira PDF com Cmd+P.

## Como usar

Peça pro Claude:

- "monta a proposta pro [cliente]" — ele lê `comercial/oferta.md`, `comercial/icp.md` e o briefing do cliente, e preenche
- "adapta essa proposta pro [outro cliente]"
- "faz a versão de WhatsApp dessa proposta" — o resumo em texto que você manda antes do link

O arquivo final vai pra `propostas/nome-do-cliente.html` (prospect) ou pra dentro da pasta do cliente, se ele já for ativo. O modelo nunca é editado no lugar.

## A ordem das seções não é decorativa

1. **Contexto** — o problema dele, com as palavras dele. Se ele não se reconhecer aqui, o resto não é lido.
2. **Proposta** — o caminho.
3. **Entregáveis** — o que chega na mão dele, com o que **não** entra escrito na cara.
4. **Prazo** — e o que você precisa dele pra cumprir.
5. **Investimento** — depois do valor construído, nunca antes.
6. **Prova** — um case com número.
7. **Próximo passo** — o que acontece se ele aprovar.

## Três erros que essa estrutura evita

- **Preço no começo.** Quem lê preço antes de entender o valor compara por número.
- **Escopo aberto.** A seção "o que não está incluso" é a que te salva de trabalhar de graça.
- **Fim sem instrução.** "Fico à disposição" não fecha nada. "Aprova aqui e começamos segunda" fecha.

## Validade

Toda proposta sai com data de validade. Não é pressão de venda, é higiene: preço de três meses atrás não é mais o seu preço.
