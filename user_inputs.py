from datetime import datetime

# url da página de compra do jogo (tem que ser aquela que começa com "cart.totacesso")
URL = "https://cart.totalacesso.com/saopaulofcxlducopaconmebolsudamericana_31_08_23"

# lista com os setores em ordem de preferência
SECTIONS_WITH_MEMBERSHIP_DISCOUNT = ["ARQUIBANCADA BITSO LESTE", "ARQUIBANCADA OESTE", "ARQUIBANCADA SUL",
                                     "CADEIRA ESPECIAL LESTE"]

SECTIONS_WITHOUT_DISCOUNT = ["ARQUIBANCADA NORTE", "CADEIRA SUPERIOR NORTE", "CADEIRA SUPERIOR SUL",
                             "CADEIRA ESPECIAL OESTE"]

# credenciais
USERNAME: str =
PASSWORD: str =

# cpf do sócio
CPF: int =

# número de convidados
NUMBER_OF_GUESTS = 2

# se quiser começar em um determinado horário
IS_SCHEDULED = True
SCHEDULED_TIMESTAMP = datetime(2023, 8, 28, 21, 59)
