from datetime import datetime

# url da página de compra do jogo (tem que ser aquela que começa com "cart.totacesso")
URL = "https://cart.spfcticket.net/saopaulofcxnovorizontino_quartas_de_final_2025"

# lista com os setores em ordem de preferência
SECTIONS_WITH_MEMBERSHIP_DISCOUNT = ["ARQUIBANCADA LESTE LACTA",
                                     "ARQUIBANCADA OESTE OURO BRANCO"
                                     "ARQUIBANCADA NORTE OURO BRANCO", "ARQUIBANCADA SUL DIAMANTE NEGRO",
                                     "CADEIRA SUPERIOR NORTE OREO"]

SECTIONS_WITHOUT_DISCOUNT =  ["ARQUIBANCADA NORTE OURO BRANCO", "ARQUIBANCADA SUL DIAMANTE NEGRO",
 "CADEIRA SUPERIOR NORTE OREO",
 "CAD. SUP. SUL DIAMANTE NEGRO", "CAD. ESP. OESTE OURO BRANCO"]

# credenciais
USERNAME: str =
PASSWORD: str =

# cpf do sócio
CPF: str =

# quantidade de ingressos
MEMBERSHIP_HOLDER: bool = True  # ingresso do titular (0 ou 1)
NUMBER_OF_GUESTS = 1  # convidado

GENERAL_AVAILABLE_TICKET = 0  # ingresso inteiro venda geral
HALF_PRICE_TICKET: bool = False  # meia entrada venda geral

# se quiser começar em um determinado horário
IS_SCHEDULED = True
SCHEDULED_TIMESTAMP = datetime(2025, 2, 27, 18, 00)
