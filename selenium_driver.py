import random
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


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
                time.sleep(time_to_wait.seconds)

    def accept_cookies(self):
        try:
            cookies_button = self.wait_and_find_element(method=By.XPATH,
                                                        timeout=random.randrange(2, 5),
                                                        element_id_or_xpath="//a[@class='cc-btn cc-dismiss']")

            cookies_button.click()
            print("cookies aceitos")
        except:
            pass

    def input_cpf(self, cpf):
        try:
            cpf_field = self.wait_and_find_element(method=By.ID,
                                                   timeout=random.randrange(2, 5),
                                                   element_id_or_xpath="inputPromocode")

            cpf_field.send_keys(cpf)

            cpf_field.submit()

            # self.driver.implicitly_wait(15)
            print("cpf ok")

            return True
        except:
            self.driver.refresh()
            print("cpf deu ruim")
            return False

    def go_to_section_tab(self, section_name):
        print(f"procurando {section_name}")
        section_was_found = False
        while not section_was_found:
            try:
                tab_button = self.wait_and_find_element(method=By.XPATH,
                                                        timeout=random.randrange(2, 5),
                                                        element_id_or_xpath=f"//button[@title='{section_name}']")

                tab_button.click()
                section_was_found = True
                return section_was_found
            except:
                try:
                    next_arrow_button = self.wait_and_find_element(method=By.ID,
                                                                   timeout=random.randrange(1, 3),
                                                                   element_id_or_xpath="sector-next")

                    next_arrow_button.click()
                except:
                    print("setor não encontrado. tentando o próximo...")
                    self.driver.refresh()
                    return False

    def add_tickets_to_cart(self, number_of_guests: int) -> bool:
        try:
            add_main_ticket_element = self.wait_and_find_element(method=By.XPATH,
                                                                 timeout=random.randrange(2, 5),
                                                                 element_id_or_xpath="/html/body/app-root/app-layout/main/app-page-cart/div[2]/app-products-group/div/div/app-product-item[1]/div/div/div[2]/div/button[2]/i")
            add_main_ticket_element.click()

            for i in range(number_of_guests):
                add_guest_element = self.wait_and_find_element(method=By.XPATH,
                                                               timeout=random.randrange(2, 5),
                                                               element_id_or_xpath="/html/body/app-root/app-layout/main/app-page-cart/div[2]/app-products-group/div/div/app-product-item[2]/div/div/div[2]/div/button[2]/i")

                add_guest_element.click()

            # continuar
            continue_button = self.wait_and_find_element(method=By.ID,
                                                         timeout=random.randrange(2, 5),
                                                         element_id_or_xpath="buttonContinue")

            self.driver.execute_script("arguments[0].click();", continue_button)

            review_continue_button = self.wait_and_find_element(method=By.XPATH,
                                                                timeout=random.randrange(2, 5),
                                                                element_id_or_xpath="//button[@data-cy='review-button-continue']")

            review_continue_button.click()

            # terms and conditions
            checkbox = self.wait_and_find_element(method=By.ID,
                                                  timeout=random.randrange(2, 5),
                                                  element_id_or_xpath="tuPpEvent")

            checkbox.click()

            review_continue_button = self.wait_and_find_element(method=By.XPATH,
                                                                timeout=random.randrange(2, 5),
                                                                element_id_or_xpath="//button[@data-cy='review-button-continue']")

            review_continue_button.click()

            return True
        except:
            print(
                "erro ao adicionar ao carrinho (provavelmente \"esgotou\"). tentando outro setor.")
            self.driver.refresh()

    def log_in(self, user: str, password: str):
        try:
            username_element = self.wait_and_find_element(method=By.ID,
                                                          timeout=15,
                                                          element_id_or_xpath="userLogin")
            username_element.send_keys(user)

            password_element = self.wait_and_find_element(method=By.ID,
                                                          timeout=5,
                                                          element_id_or_xpath="password")
            password_element.send_keys(password)

            password_element.submit()

            if "payment" in self.driver.current_url:
                print("sucesso")
                return True

        except:
            print("deu ruim. deve estar dizendo que o produto não está disponível. tentando de novo...")
            self.driver.get(self.main_url)
            return False

    def wait_and_find_element(self, method, timeout, element_id_or_xpath):
        return WebDriverWait(self.driver, timeout=timeout).until(
            EC.element_to_be_clickable((method, element_id_or_xpath)))
