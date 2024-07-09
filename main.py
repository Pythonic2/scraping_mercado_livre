import os
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver

# Obtém a URL do Selenium Remote a partir da variável de ambiente
selenium_remote_url = os.getenv('SELENIUM_REMOTE_URL', 'http://192.168.80.2:4444/wd/hub')

options = ChromeOptions()
options.set_capability('se:recordVideo', True)
options.set_capability('se:screenResolution', '1920x1080')
options.set_capability('se:name', 'test_visit_basic_auth_secured_page (ChromeTests)')

options.set_capability('browserName','chrome')

driver = webdriver.Remote(options=options, command_executor=selenium_remote_url)
driver.get("https://selenium.dev")
print(driver.title)
from time import sleep
sleep(60)
driver.quit()
