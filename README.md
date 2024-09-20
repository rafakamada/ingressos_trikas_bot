# ingressos_trikas_bot

Script em Python usando Selenium para comprar ingressos para os jogos do Trikas

## Introdução

Está cada vez mais difícil comprar ingressos para os jogos do SPFC, mesmo para os sócio-torcedores. Pra piorar, o site é
uma porcaria. Esse programa nos poupa de fazer manualmente o loop de atualizar e tentar inserir ingressos no carrinho ou
ficar a espreita no site esperando dar o horário de liberação dos ingressos para a prioridade do seu plano.

## Disclaimer

Fiz esse programa na intenção de ajudar a mim mesmo e a meus amigos a conseguir ingressos para os jogos, dada a
dificuldade mencionada logo acima.
O código está aberto porque pode ajudar outras pessoas a ter êxito nessa tarefa, bem como atrair contribuições de
interessados em melhorar e manter o código.
**Não me responsabilizo em caso de uso dessa aplicação para fins fraudulentos (como cambismo, agiotagem, prevaricação,
talaricagem, estelionato, etc)**

## Requisitos

- Plano de sócio torcedor para poder inserir o CPF (ou modificar o script pra poder comprar sem ser sócio)
- Conta no total acesso

## Como usar

1. Editar o arquivo `user_inputs.py` e inserir
    - CPF do sócio
    - email e senha para logar no SPFC Ticket(ex-Total Acesso)
    - url de compra do jogo
    - se desejar agendar o início do programa, ligar a flag `IS_SCHEDULED` e definir o horário de início
      em `SCHEDULED_TIMESTAMP`
2. Dar play na `main.py`