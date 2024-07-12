import undetected_chromedriver as uc
uc.TARGET_VERSION = 126.0
options = uc.ChromeOptions()
options.arguments.extend(["--no-sandbox", "--disable-setuid-sandbox","--headless"]) 
driver = uc.Chrome(options)
driver.get("https://google.com.br")
print(driver.title)
