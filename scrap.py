import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.chrome.service import Service


class Bot_chrome:

    def __init__(self) -> None:
        self.options = uc.ChromeOptions()
        self.options.add_argument('--headless=False')
        self.driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    
    def acessar(self):
        self.driver.get("https://www.mercadolivre.com/jms/mlb/lgz/msl/login/H4sIAAAAAAAEAzWNSw6DMAxE7-I1gn2WvUhkgoGoDkGOIVQVd69TieV83swXOC9x8_rZCRzQtXMMUaGDnVHnLMnHyYLEZpWo9MixVVAwkZIUcN82tND0IoPa1IxcyEp46OpnztW8_5d5sXi6jNuQfaXxjNTSh1iyiVV1L24Yaq19Igk4ZY6nUB9y6kcZ4O4MKOpVMLzBqRx0_wBJfknyzgAAAA/user")
        self.driver.save_screenshot("teste.png")
        self.driver.close()


