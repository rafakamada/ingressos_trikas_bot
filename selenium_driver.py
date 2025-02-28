import logging
import random
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class SeleniumDriver:
    def __init__(self, url: str, is_scheduled: bool = False, scheduled_start: datetime = None):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)  # pra não fechar o browser quando conseguir
        chrome_options.add_argument("--incognito")

        self.main_url = url
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(url)
        self.driver.maximize_window()
        if is_scheduled:
            time_to_wait = scheduled_start - datetime.now()
            if scheduled_start > datetime.now():
                logging.info(f"aguardando horário agendado: {scheduled_start}")
                time.sleep(time_to_wait.seconds)
                logging.info("AUTORIZA O ARBITRO")

    def accept_cookies(self):
        try:
            cookies_button = self.wait_and_find_clickable_element(method=By.XPATH,
                                                                  timeout=random.randrange(1, 2),
                                                                  element_id_or_xpath="//a[@class='cc-btn cc-dismiss']")

            cookies_button.click()
            logging.info("cookies aceitos")
        except:
            pass

    def input_cpf(self, cpf):
        try:
            cpf_field = self.wait_and_find_clickable_element(method=By.ID,
                                                             timeout=random.randrange(1, 2),
                                                             element_id_or_xpath="inputPromocode")

            cpf_field.send_keys(cpf)

            cpf_field.submit()

            self.wait_and_find_clickable_element(method=By.XPATH,
                                                 timeout=15,  # esse pode demorar
                                                 element_id_or_xpath="//button[@data-cy='promocode-button']")
            logging.info("cpf ok")

            return True

        except:
            self.driver.refresh()
            logging.info("cpf deu ruim")
            return False

    def go_to_section_tab(self, section_name):

        logging.info(f"procurando {section_name}")

        section_tab_was_found = False
        while not section_tab_was_found:
            try:
                tab_button = self.wait_and_find_clickable_element(method=By.XPATH,
                                                                  timeout=random.randrange(1, 2),
                                                                  element_id_or_xpath=f"//button[@title='{section_name}']")

                tab_button.click()
                section_tab_was_found = True
                return section_tab_was_found
            except:
                try:
                    next_arrow_button = self.wait_and_find_clickable_element(method=By.ID,
                                                                             timeout=random.randrange(1, 2),
                                                                             element_id_or_xpath="sector-next")

                    next_arrow_button.click()
                except:
                    logging.info("setor não encontrado. tentando o próximo...")
                    self.driver.refresh()
                    return False

    def add_tickets_to_cart(self, membership_holder: bool, number_of_guests: int, is_without_discount: bool,
                            general_available_tickets: int, half_price_ticket: bool) -> bool:

        logging.info("tentando adicionar ingressos ao carrinho")
        if not is_without_discount:  # baita gambiarra por enquanto
            try:
                self.add_membership_tickets(number_of_guests)
            except:
                logging.info(
                    "erro ao adicionar ao carrinho ingressos de sócio ou convidado.")
                self.driver.refresh()
                return False
        else:  # adicionar ingressos sem desconto como plano B caso não tenha nenhum setor com desconto disponível
            try:
                self.add_tickets_without_discount(number_of_guests)
            except:
                logging.info(
                    "erro ao adicionar ingressos sem desconto. tentando outro setor.")
                self.driver.refresh()
                return False
        if general_available_tickets > 0 or half_price_ticket:
            try:
                self.add_general_available_tickets(general_available_tickets, half_price_ticket,
                                                   membership_holder)
            except:
                logging.info(
                    "erro ao adicionar ingressos gerais. tentando outro setor.")
                self.driver.refresh()
                return False

        # continuar
        try:
            continue_button = self.wait_and_find_clickable_element(method=By.ID,
                                                                   timeout=random.randrange(1, 2),
                                                                   element_id_or_xpath="buttonContinue")
            self.driver.execute_script("arguments[0].click();", continue_button)
            review_continue_button = self.wait_and_find_clickable_element(method=By.XPATH,
                                                                          timeout=random.randrange(1, 2),
                                                                          element_id_or_xpath="//button[@data-cy='review-button-continue']")
            review_continue_button.click()
            # terms and conditions
            checkbox = self.wait_and_find_clickable_element(method=By.ID,
                                                            timeout=random.randrange(1, 2),
                                                            element_id_or_xpath="tuPpEvent")
            checkbox.click()
            review_continue_button = self.wait_and_find_clickable_element(method=By.XPATH,
                                                                          timeout=random.randrange(1, 2),
                                                                          element_id_or_xpath="//button[@data-cy='review-button-continue']")
            review_continue_button.click()
            return True

        except:
            logging.info(
                "erro ao adicionar ao carrinho (provavelmente \"esgotou\"). tentando outro setor.")
            self.driver.refresh()
            return False

    def add_tickets_without_discount(self, number_of_guests):
        full_price_tickets_attempt_1 = "/html/body/app-root/app-layout/main/app-page-cart/div[2]/app-products-group/div/div/app-product-item[2]/div/div/div[2]/div/button[2]/i"
        full_price_tickets_attempt_2 = "/html/body/app-root/app-layout/main/app-page-cart/div[2]/app-products-group/div/div/app-product-item[1]/div/div/div[2]/div/button[2]/i"

        try:
            add_ticket_element = self.wait_and_find_clickable_element(method=By.XPATH,
                                                                      timeout=random.randrange(1, 2),
                                                                      element_id_or_xpath=full_price_tickets_attempt_1)
        except:
            add_ticket_element = self.wait_and_find_clickable_element(method=By.XPATH,
                                                                      timeout=random.randrange(1, 2),
                                                                      element_id_or_xpath=full_price_tickets_attempt_2)
        for i in range(number_of_guests + 1):
            add_ticket_element.click()

    def add_membership_tickets(self, number_of_guests):
        add_main_ticket_element = self.wait_and_find_clickable_element(method=By.XPATH,
                                                                       timeout=random.randrange(1, 2),
                                                                       element_id_or_xpath="/html/body/app-root/app-layout/main/app-page-cart/div[2]/app-products-group/div/div/app-product-item[1]/div/div/div[2]/div/button[2]/i")
        add_main_ticket_element.click()

        for i in range(number_of_guests):
            add_guest_element = self.wait_and_find_clickable_element(method=By.XPATH,
                                                                     timeout=random.randrange(1, 2),
                                                                     element_id_or_xpath="/html/body/app-root/app-layout/main/app-page-cart/div[2]/app-products-group/div/div/app-product-item[2]/div/div/div[2]/div/button[2]/i")

            add_guest_element.click()

    def add_general_available_tickets(self, number_of_general_tickets, include_half_price_ticket,
                                      membership_holder):
        general_ticket_element_index = 3 if membership_holder else 1
        general_ticket_element_xpath = f"/html/body/app-root/app-layout/main/app-page-cart/div[2]/app-products-group/div/div/app-product-item[{general_ticket_element_index}]/div/div/div[2]/div/button[2]/i"

        add_general_ticket_element = self.wait_and_find_clickable_element(method=By.XPATH,
                                                                          timeout=random.randrange(1, 2),
                                                                          element_id_or_xpath=general_ticket_element_xpath)

        for i in range(number_of_general_tickets):
            add_general_ticket_element.click()

        half_price_element_index = general_ticket_element_index + 1
        half_price_element_xpath = f"/html/body/app-root/app-layout/main/app-page-cart/div[2]/app-products-group/div/div/app-product-item[{half_price_element_index}]/div/div/div[2]/div/button[2]/i"

        if include_half_price_ticket:
            add_half_price_ticket_element = self.wait_and_find_clickable_element(method=By.XPATH,
                                                                                 timeout=random.randrange(1, 2),
                                                                                 element_id_or_xpath=half_price_element_xpath)

            add_half_price_ticket_element.click()

    def log_in(self, user: str, password: str):
        # caso esteja "indisponível":
        try:
            self.wait_and_find_element_to_be_available(method=By.ID,
                                                       timeout=5,
                                                       element_id_or_xpath="swal2-html-container")  # dialog box de produto indisponível

            self.driver.get(self.main_url)
            return False
        except:
            pass

        try:
            username_element = self.wait_and_find_clickable_element(method=By.ID,
                                                                    timeout=15,
                                                                    element_id_or_xpath="userLogin")
            username_element.send_keys(user)

            password_element = self.wait_and_find_clickable_element(method=By.ID,
                                                                    timeout=5,
                                                                    element_id_or_xpath="password")
            password_element.send_keys(password)

            password_element.submit()

            if "payment" in self.driver.current_url:
                logging.info("sucesso")
                return True
            else:
                self.driver.get(self.main_url)
                return False

        except:
            self.driver.get(self.main_url)
            return False

    def check_if_section_is_available(self, section_name: str) -> bool:
        available_section_divs = self.driver.find_elements(By.XPATH,
                                                           "//app-product-item")

        desired_section_div = list(
            filter(lambda x: (section_name in x.text) and ('ESGOTADO' not in x.text.upper()), available_section_divs))

        if len(desired_section_div) > 0:
            return True
        else:
            return False

    def define_target_section(self, desired_sections: list[str]) -> str:
        for section in desired_sections:
            if self.check_if_section_is_available(section):
                return section
        logging.info("nenhum dos setores desejados está disponível")
        self.driver.refresh()
        return "none"

    def wait_and_find_clickable_element(self, method, timeout, element_id_or_xpath):
        return WebDriverWait(self.driver, timeout=timeout).until(
            EC.element_to_be_clickable((method, element_id_or_xpath)))

    def wait_and_find_element_to_be_available(self, method, timeout, element_id_or_xpath):
        return WebDriverWait(self.driver, timeout=timeout).until(
            EC.presence_of_element_located((method, element_id_or_xpath)))
