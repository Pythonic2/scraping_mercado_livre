from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.firefox.options import Options
# connect to grid
driver = webdriver.Remote(
    command_executor='http://172.18.0.2:4444',
    options=Options(),
)
driver.get("https://google.com.br")
print(driver.title)