from playsound import playsound

from selenium_driver import SeleniumDriver
from user_inputs import URL, CPF, GRANDSTAND_SECTIONS, NUMBER_OF_GUESTS, USERNAME, PASSWORD, IS_SCHEDULED, \
    SCHEDULED_TIMESTAMP

driver = SeleniumDriver(URL, IS_SCHEDULED, SCHEDULED_TIMESTAMP)

success = False
section_index = 0


def update_section_index(current_index):
    if current_index + 1 < len(GRANDSTAND_SECTIONS):
        return current_index + 1
    else:
        return 0


while not success:
    driver.accept_cookies()

    cpf_success = driver.input_cpf(CPF)
    if not cpf_success:
        continue  # reiniciar loop

    section_was_found = driver.go_to_section_tab(GRANDSTAND_SECTIONS[section_index])

    if not section_was_found:
        section_index = update_section_index(section_index)
        continue

    tickets_were_added = driver.add_tickets_to_cart(NUMBER_OF_GUESTS)
    if not tickets_were_added:
        section_index = update_section_index(section_index)
        continue

    success = driver.log_in(USERNAME, PASSWORD)

playsound('success_song.mp3')
