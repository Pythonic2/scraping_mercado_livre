import os
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver

options = ChromeOptions()
options.set_capability('se:recordVideo', True)
options.set_capability('se:screenResolution', '1920x1080')
options.set_capability('se:name', 'test_visit_basic_auth_secured_page (ChromeTests)')

selenium_host = os.getenv('SELENIUM_HOST', 'localhost')
driver = webdriver.Remote(options=options, command_executor=f"http://{selenium_host}:4444/wd/hub")
driver.get("https://selenium.dev")
print(driver.title)
driver.quit()
