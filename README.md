# ingressos_trikas_bot

Script em Python usando Selenium para comprar ingressos para os jogos do Trikas

# Requisitos

- Ter algum plano de sócio torcedor para poder inserir o CPF (ou modificar o script pra poder comprar sem ser sócio)
- Conta no total acesso

# Como usar

1. Editar o arquivo `user_inputs.py` e inserir
    - CPF do sócio
    - email e senha para logar no Total Acesso
    - url de compra do jogo
    - se desejar agendar o início do programa, ligar a flag `IS_SCHEDULED` e definir o horário de início
      em `SCHEDULED_TIMESTAMP`
2. Dar play na `main.py`