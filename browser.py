from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime
from multiprocessing import Lock
from selenium.webdriver.chrome.service import Service


move_lock = Lock()
# exceptions
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    TimeoutException,
    InvalidElementStateException,
)

class WindowNotFound(Exception):
    """Browser window not found."""


import os
from contextlib import contextmanager
from typing import Iterator, List, Callable, Any
import pathlib
import uuid
import shutil

class Browser:
    driver: webdriver.Chrome
    driver_wait: WebDriverWait
    actions: ActionChains
    

    def __init__(self):
        self.teste = 0
        self.setup_browser()

    @contextmanager
    def on_new_window(self, url: str) -> Iterator[None]:
        """Open a new window with the given url."""
        last_handle = self.driver.current_window_handle
        self.driver.execute_script(f"window.open('{url}')")
        new_handle = None
        while not new_handle:
            for handle in self.driver.window_handles:
                if handle is not last_handle:
                    # check if it has the url
                    self.driver.switch_to.window(handle)
                    if self.driver.current_url == url:
                        if self.driver.execute_script("return document.readyState") == "complete":
                            new_handle = handle
                            break
            sleep(1)
        yield
        self.driver.close()
        self.driver.switch_to.window(last_handle)

    @contextmanager
    def on_window(self, has_element: str, retry: int = 10):
        """Switch to a window that has the given element."""
        default_handle = self.driver.current_window_handle
        found_handle = None
        while not found_handle:
            try:
                for handle in self.driver.window_handles:
                    if handle is default_handle:
                        continue
                    self.driver.switch_to.window(handle)
                    if self.driver.find_elements(By.XPATH, has_element):
                        found_handle = handle
                        break
            except:
                sleep(1)
                retry -= 1
                if retry < 1:
                    raise WindowNotFound(f"Window with xpath {has_element} not found")
        yield
        self.driver.switch_to.window(default_handle)

    @contextmanager
    def on_iframe(self, xpath: str) -> Iterator[None]:
        """Switch to an iframe."""
        iframe = self.driver_wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        self.driver.switch_to.frame(iframe)
        try:
            yield
        finally:
            self.driver.switch_to.default_content()

    def wait_alert(self, retry: int = 1) -> Any:
        """Wait for an alert to appear."""
        while retry > 0:
            try:
                return self.driver_wait.until(EC.alert_is_present())
            except TimeoutException:
                retry -= 1
        raise TimeoutException("Alert not found")

    def __get_condition(self, condition: str) -> Callable:
        match condition:
            case "visible":
                return EC.visibility_of_element_located
            case "visible_any":
                return EC.visibility_of_any_elements_located
            case "visible_all":
                return EC.visibility_of_all_elements_located
            case "clickable":
                return EC.element_to_be_clickable
            case "selected":
                return EC.element_to_be_selected
            case "located_all":
                return EC.presence_of_all_elements_located
            case _:
                return EC.presence_of_element_located

    def __get_element(self, xpath: str, ec: str, retry: int = 1):
        """Wait until the element is located."""
        while True:
            try:
                ec = self.__get_condition(ec)
                return self.driver_wait.until(ec((By.XPATH, xpath)))
            except (TimeoutException, NoSuchElementException):
                retry -= 1
                if retry < 1:
                    raise NoSuchElementException(f"Element with xpath {xpath} not found")

    def find_elements(self, xpath: str, condition: str = "located_all", wait: bool = True) -> List[WebElement]:
        """Wait until the any of the elements are located."""
        if wait:
            return self.__get_element(xpath, ec=condition)
        return self.driver.find_elements(By.XPATH, xpath)

    def find_element(self, xpath: str, condition: str = None, retry: int = 1) -> List[WebElement]:
        """Wait until the element is located."""
        return self.__get_element(xpath, ec=condition, retry=retry)

    def hover(self, xpath: str, condition: str = "visible", dom=True) -> None:
        """Hover over the element."""
        element = self.find_element(xpath, condition)
        if not dom:
            self.actions.reset_actions()
            self.actions.move_to_element(element).perform()
        else:
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);"
                "arguments[0].style.border='3px solid red';"
                "if (arguments[0].onmouseover) {arguments[0].onmouseover();}",
                element,
            )

    def click(self, xpath: str) -> None:
        """Click the element."""

        element = self.find_element(xpath, condition="clickable")
        try:
            self.driver.execute_script(
                "if (arguments[0].onmouseover) {arguments[0].onmouseover();}",
                "if (arguments[0].onclick) {arguments[0].onclick();} else {arguments[0].click();}",
                "arguments[0].scrollIntoView(true);",
                element,
            )
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            element.click()

    def get_text(self, xpath: str, timeout: int = 10, allow_empty:bool = False) -> str:
        """Get the text from the element."""
        while timeout > 0:
            try:
                text = self.find_element(xpath).text
                if text or allow_empty:
                    return text
            except NoSuchElementException:                
                timeout -= 1
        raise NoSuchElementException(f"Element with xpath {xpath} not found")

    def send_text(self, xpath: str, text: str, clear: bool = False, timeout=10, verify=False) -> WebElement:
        """Send text to the element."""

        while timeout > 0:
            try:
                element = self.find_element(xpath, "clickable")
                if clear:
                    element.clear()
                element.send_keys(text)
            except InvalidElementStateException as exc:
                if "Element is read-only" in str(exc):
                    self.driver.execute_script("arguments[0].removeAttribute('readonly')", element)
                    continue

            if not verify or element.get_attribute("value") == text:
                return element
            timeout -= 1
        raise TimeoutException(f"Timeout sending text to element with xpath {xpath}")

    def __select_option(self, xpath: str, option: str, by_value: bool = False) -> None:
        """Select an option from a select element."""
        element = self.find_element(xpath, condition="clickable")
        select = Select(element)
        if by_value:
            select.select_by_value(option)
        else:
            select.select_by_visible_text(option)

    def select_option(
        self, xpath: str, option: str, retry: int = 10, timeout: int = 10, verify: bool = False, by_value: bool = False
    ) -> WebElement:
        """Select an option from a select element."""
        while timeout > 0:
            self.__select_option(xpath, option, by_value)
            if not verify or self.find_element(xpath).get_attribute("value") == option:
                return self.find_element(xpath)
            sleep(2)
            timeout -= 1
        raise NoSuchElementException(f"Option {option} not found in select element with xpath {xpath}")


    def wait_for_download(self, timeout=300) -> str | bool:
        """
        Wait for download to complete by monitoring the temp download directory.
        
        Args:
            timeout (int): Maximum time to wait in seconds (default 5 minutes)
        
        Returns:
            bool: True if download completed, False if timed out
        """
        start_time = datetime.now()
        while True:
            # Check for any .crdownload or .tmp files which indicate ongoing downloads
            files = os.listdir(self.TEMP_DOWNLOAD_DIR)
            if not any(f.endswith('.crdownload') or f.endswith('.tmp') for f in files):
                # If there are any xlsx files and no temporary files, download is complete
                if any(f.endswith('.xlsx') for f in files):
                    # return file name
                    return files[0]
            
            # Check if we've exceeded the timeout
            if (datetime.now() - start_time).total_seconds() > timeout:
                return False
                
            sleep(1)  # Wait 1 second before checking again

    def wait_for_download_and_move(self, to_path: str, timeout=300) -> str | bool:
        file = self.wait_for_download(timeout)
        if not file:
            return False

        source = os.path.join(self.TEMP_DOWNLOAD_DIR, file)
        destination = os.path.join(to_path, file)

        with move_lock:  # Apenas um processo pode executar essa parte por vez
            print(f"Processo {os.getpid()}wair for donload and move {file} de {source} para {destination}")

            shutil.move(source, destination)
        
        return destination
    # def wait_for_download_and_move(self, to_path:str, timeout=300) -> str | bool:
    #     file = self.wait_for_download(timeout)
    #     if not file:
    #         return False
    #     source = f"{self.TEMP_DOWNLOAD_DIR}{file}"
    #     destination = f"{to_path}{file}"
    #     shutil.move(source, destination)
    #     return destination
        
        
    def wait_loading(self, xpath: str, timeout: int = 160):
        print("estou aguardando o loading")
        WebDriverWait(self.driver, timeout).until_not(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

            
    def set_download_folder(self, options: webdriver.ChromeOptions) -> None:        
        self.TEMP_DOWNLOAD_DIR = f"{pathlib.Path(__file__).parent.absolute()}\\temp_downloads_{uuid.uuid4()}\\"
        if not os.path.exists(self.TEMP_DOWNLOAD_DIR):
            os.makedirs(self.TEMP_DOWNLOAD_DIR)
        
        prefs = {
            "profile.default_content_settings.popups": 0,
            "download.default_directory": self.TEMP_DOWNLOAD_DIR,
             "directory_upgrade": True
            }
        options.add_experimental_option("prefs", prefs)

    def setup_browser(self) -> None:
        chrome_driver_path = "C:\\GATEBOT\\Chromedriver\\chromedriver.exe"

        """Setup the browser with the necessary configurations"""        
        browser_options = webdriver.ChromeOptions()
        service = Service(executable_path=chrome_driver_path)
        browser_options.add_argument("--headless=new")
        browser_options.add_argument("--window-size=1920,1080")  # Força tamanho correto
        browser_options.add_argument("--no-sandbox")
        browser_options.add_argument("--disable-dev-shm-usage")
        browser_options.add_argument("--disable-gpu")
        browser_options.add_argument("--disable-notifications")
        browser_options.add_argument("--disable-popup-blocking")
        browser_options.add_argument("--ignore-certificate-errors")   
        self.set_download_folder(browser_options)
        self.driver = webdriver.Chrome(service=service,options=browser_options)
        self.driver_wait = WebDriverWait(self.driver, 10)
        self.actions = ActionChains(self.driver)
        self.driver.set_window_size(1920, 1080)
