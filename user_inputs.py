from datetime import datetime

# url da página de compra do jogo (tem que ser aquela que começa com "cart.totacesso")
URL = "https://cart.spfcticket.net/saopaulofcxinternacional_22_09"

# lista com os setores em ordem de preferência
SECTIONS_WITH_MEMBERSHIP_DISCOUNT = ["ARQUIBANCADA LESTE LACTA", "ARQUIBANCADA OESTE OURO BRANCO",
                                     "ARQUIBANCADA NORTE OURO BRANCO", "ARQUIBANCADA SUL DIAMANTE NEGRO",
                                     "CADEIRA SUPERIOR NORTE OREO"]

SECTIONS_WITHOUT_DISCOUNT = ["ARQUIBANCADA NORTE OURO BRANCO", "ARQUIBANCADA SUL DIAMANTE NEGRO",
                             "CADEIRA SUPERIOR NORTE OREO",
                             "CAD. SUP. SUL DIAMANTE NEGRO", "CAD. ESP. OESTE OURO BRANCO"]

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
