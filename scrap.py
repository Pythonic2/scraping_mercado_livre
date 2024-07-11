from selenium.webdriver import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class BotChrome:

    def __init__(self):
        self.chrome_options = Options()
        #self.chrome_options.add_argument('--headless')
       
        #self.chrome_options.add_argument(r'--user-data-dir=C:\Users\igorsilv\OneDrive - Capgemini\Desktop\rivalry\DadosNavegador')
        #drive
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 120)
        

    def get_element_by_xpath(self, xpath, ec=None):
        ec = ec if ec else EC.presence_of_element_located
        return self.wait.until(ec((By.XPATH, xpath)))


    def acessar(self):
        self.driver.get("https://github.com/")
        print("ok")
        
    def login(self):
        btn_login = self.get_element_by_xpath("//a[contains(text(),'Sign in')]")
        btn_login.click()
        email = self.get_element_by_xpath("//input[@id='login_field']")
        email.send_keys('igormarinhosilva@gmail.com')
        password = self.get_element_by_xpath("//input[@id='password']")
        password.send_keys("i313131094141")
        btn_sigin = self.get_element_by_xpath("//input[@value='Sign in']")

if __name__=='__main__':
    bot = BotChrome()
    bot.acessar()