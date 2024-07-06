from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver

options = ChromeOptions()
options.set_capability('se:recordVideo', True)
options.set_capability('se:screenResolution', '1920x1080')
options.set_capability('se:name', 'test_visit_basic_auth_secured_page (ChromeTests)')
driver = webdriver.Remote(options=options, command_executor="http://localhost:4445")
driver.get("https://selenium.dev")
print(driver.title)
driver.quit()

# from selenium.webdriver import Keys
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# import csv
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options

# class BotChrome:

#     def __init__(self):
#         self.chrome_options = Options()
#         self.chrome_options.add_argument('--headless')
#         self.chrome_options.add_argument('--no-sandbox')

#         self.chrome_options.add_argument(r'--user-data-dir=\DadosNavegador')
#         #drive
#         self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
#         self.wait = WebDriverWait(self.driver, 120)
        

#     def get_element_by_xpath(self, xpath, ec=None):
#         ec = ec if ec else EC.presence_of_element_located
#         return self.wait.until(ec((By.XPATH, xpath)))
    
#     def acessar(self):
#         self.driver.get('https://google.com')
#         print(self.driver.title)

# if __name__ == '__main__':
#     bot = BotChrome()
#     bot.acessar()
    