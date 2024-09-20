from playsound import playsound

from selenium_driver import SeleniumDriver
from user_inputs import URL, CPF, SECTIONS_WITH_MEMBERSHIP_DISCOUNT, NUMBER_OF_GUESTS, USERNAME, PASSWORD, IS_SCHEDULED, \
    SCHEDULED_TIMESTAMP, SECTIONS_WITHOUT_DISCOUNT

driver = SeleniumDriver(URL, IS_SCHEDULED, SCHEDULED_TIMESTAMP)

success = False
section_index = 0

while not success:
    driver.accept_cookies()

    cpf_success = driver.input_cpf(CPF)
    if not cpf_success:
        continue  # reiniciar loop

    target_section_found = driver.define_target_section(
        desired_sections=SECTIONS_WITH_MEMBERSHIP_DISCOUNT + SECTIONS_WITHOUT_DISCOUNT)

    if target_section_found == "none":
        continue

    is_without_discount = target_section_found not in SECTIONS_WITH_MEMBERSHIP_DISCOUNT

    target_section_tab_was_found = driver.go_to_section_tab(target_section_found)

    if not target_section_tab_was_found:
        continue

    tickets_were_added = driver.add_tickets_to_cart(NUMBER_OF_GUESTS, is_without_discount)
    if not tickets_were_added:
        continue

    success = driver.log_in(USERNAME, PASSWORD)

playsound('success_song.mp3')
