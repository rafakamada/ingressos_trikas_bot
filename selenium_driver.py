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
            if time_to_wait.seconds < 80000:  # não fica negativo
                time.sleep(time_to_wait.seconds)

    def accept_cookies(self):
        try:
            cookies_button = WebDriverWait(self.driver, timeout=random.randrange(2, 5)).until(
                EC.presence_of_element_located((By.XPATH, "//a[@class='cc-btn cc-dismiss']")))

            cookies_button.click()
            print("cookies aceitos")
        except:
            pass

    def input_cpf(self, cpf):
        try:
            cpf_field = WebDriverWait(self.driver, timeout=random.randrange(2, 5)).until(
                EC.presence_of_element_located((By.ID, "inputPromocode")))
            cpf_field.send_keys(cpf)

            cpf_field.submit()

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
                tab_button = WebDriverWait(self.driver, timeout=random.randrange(5, 10)).until(  # esse demora mesmo
                    EC.element_to_be_clickable((By.XPATH, f"//button[@title='{section_name}']"))
                )

                tab_button.click()
                section_was_found = True
                return section_was_found
            except:
                try:
                    next_arrow_button = WebDriverWait(self.driver, timeout=random.randrange(1, 3)).until(
                        EC.element_to_be_clickable((By.ID, "sector-next")))
                    next_arrow_button.click()
                except:
                    print("setor não encontrado. tentando o próximo...")
                    self.driver.refresh()
                    return False

    def add_tickets_to_cart(self, number_of_guests: int) -> bool:
        try:
            add_main_ticket_element = WebDriverWait(self.driver, timeout=random.randrange(2, 5)).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "/html/body/app-root/app-layout/main/app-page-cart/div[2]/app-products-group/div/div/app-product-item[1]/div/div/div[2]/div/button[2]/i")))
            add_main_ticket_element.click()

            for i in range(number_of_guests):
                add_guest_element = WebDriverWait(self.driver, timeout=random.randrange(2, 5)).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                "/html/body/app-root/app-layout/main/app-page-cart/div[2]/app-products-group/div/div/app-product-item[2]/div/div/div[2]/div/button[2]/i")))
                add_guest_element.click()

            # continuar
            continue_button = WebDriverWait(self.driver, timeout=random.randrange(2, 5)).until(
                EC.presence_of_element_located((By.ID, "buttonContinue")))

            self.driver.execute_script("arguments[0].click();", continue_button)

            review_continue_button = WebDriverWait(self.driver, timeout=random.randrange(2, 5)).until(
                EC.presence_of_element_located((By.XPATH, "//button[@data-cy='review-button-continue']")))

            review_continue_button.click()

            # terms and conditions
            checkbox = WebDriverWait(self.driver, timeout=random.randrange(2, 5)).until(
                EC.presence_of_element_located((By.ID, "tuPpEvent")))
            checkbox.click()

            review_continue_button = WebDriverWait(self.driver, timeout=random.randrange(2, 5)).until(  # find again
                EC.presence_of_element_located((By.XPATH, "//button[@data-cy='review-button-continue']")))

            review_continue_button.click()

            return True
        except:
            print(
                "erro ao adicionar adicionar (provavelmente tá dizendo que esgotou depois de mostrar como disponível antes). tentando outro setor.")
            self.driver.refresh()

    def log_in(self, user: str, password: str):
        try:
            username_element = WebDriverWait(self.driver, timeout=10).until(
                EC.presence_of_element_located((By.ID, "userLogin")))
            username_element.send_keys(user)

            password_element = self.driver.find_element(By.ID, "password")
            password_element.send_keys(password)

            password_element.submit()

            if "payment" in self.driver.current_url:
                print("sucesso")
                return True

        except:
            print("deu ruim. tentando de novo...")
            self.driver.get(self.main_url)
            return False
