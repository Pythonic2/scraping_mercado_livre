import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from time import sleep


class Bot_chrome:

    def __init__(self) -> None:
        self.options = uc.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    
    def acessar(self):
        self.driver.get("https://nowsecure.nl")
        print(self.driver.title)
        # email = self.driver.find_element(By.XPATH, '//input[@name="user_id"]')
        # email.send_keys('igormarinhosilva@gmail.com', Keys.ENTER)
        sleep(3)
        self.driver.save_screenshot("teste.png")

        self.driver.close()