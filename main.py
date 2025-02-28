import subprocess
import atexit
import platform
from playsound import playsound
from selenium_driver import SeleniumDriver
from user_inputs import URL, CPF, SECTIONS_WITH_MEMBERSHIP_DISCOUNT, MEMBERSHIP_HOLDER, NUMBER_OF_GUESTS, \
    GENERAL_AVAILABLE_TICKET, HALF_PRICE_TICKET, USERNAME, PASSWORD, IS_SCHEDULED, \
    SCHEDULED_TIMESTAMP, SECTIONS_WITHOUT_DISCOUNT

# Determine the operating system
os_name = platform.system()

# Start the appropriate command to prevent the system from sleeping
if os_name == 'Darwin':  # macOS
    caffeinate_process = subprocess.Popen(['caffeinate'])
elif os_name == 'Linux':
    caffeinate_process = subprocess.Popen(['xdg-screensaver', 'suspend', ':0'])
elif os_name == 'Windows':
    subprocess.run(['powercfg', '/change', 'monitor-timeout-ac', '0'])
    subprocess.run(['powercfg', '/change', 'monitor-timeout-dc', '0'])
    caffeinate_process = None
else:
    caffeinate_process = None


# Ensure the command is terminated or settings are restored when the script ends
def cleanup():
    if os_name == 'Darwin' or os_name == 'Linux':
        caffeinate_process.terminate()
    elif os_name == 'Windows':
        subprocess.run(['powercfg', '/change', 'monitor-timeout-ac', '20'])
        subprocess.run(['powercfg', '/change', 'monitor-timeout-dc', '10'])


driver = SeleniumDriver(URL, IS_SCHEDULED, SCHEDULED_TIMESTAMP)

success = False

while not success:
    driver.accept_cookies()

    driver.driver.execute_script("document.body.style.zoom='50%'")

    if MEMBERSHIP_HOLDER:
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

    tickets_were_added = driver.add_tickets_to_cart(MEMBERSHIP_HOLDER, NUMBER_OF_GUESTS, is_without_discount,
                                                    GENERAL_AVAILABLE_TICKET, HALF_PRICE_TICKET)
    if not tickets_were_added:
        continue

    success = driver.log_in(USERNAME, PASSWORD)
    driver.driver.execute_script("document.body.style.zoom='100%'")

atexit.register(cleanup)
playsound('success_song.mp3')
