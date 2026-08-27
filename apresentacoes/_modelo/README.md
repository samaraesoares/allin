# apresentacoes/_modelo/

`deck.html` é o modelo de apresentação do sistema. Preto e branco de propósito: é um esqueleto que funciona, e você troca pela sua identidade quando ela estiver definida.

## Como usar

Peça pro Claude. Exemplos que funcionam:

- "monta uma apresentação sobre [assunto] pra [quem vai assistir]"
- "transforma essa reunião em deck"
- "faz um deck de 8 slides pra aula de [tema]"

Ele copia este modelo pra `apresentacoes/nome-do-deck.html`, preenche os slides e usa as cores de `marca/design-guide.md`. O modelo nunca é editado no lugar.

## Como abrir

Dê dois cliques no arquivo. Abre no navegador, sem instalar nada.

- **F** entra no modo apresentação em tela cheia
- **Setas** ou **clique** passam os slides
- **Esc** sai
- **Cmd+P** (Mac) ou **Ctrl+P** (Windows) salva como PDF: escolha paisagem e margens zero

## Os slides que vêm prontos

Capa · abertura de seção · título com lista · número grande · três colunas · tabela · citação · encerramento com CTA. Copie o bloco `<section class="slide">` que servir e apague o resto.

## As duas regras do modelo

1. **Um slide, uma ideia.** Se você precisou de dois parágrafos, são dois slides.
2. **Máximo 30 palavras por slide.** O que você fala não vai escrito; o slide é apoio, não roteiro.

## Trocar as cores

Só o bloco `:root` no topo do arquivo. Os nomes das variáveis são os mesmos de `marca/design-guide.md`. Trocou lá, troque aqui, e todo material novo já nasce certo.
