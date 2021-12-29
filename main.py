import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
import sys
import json
import getpass
from glob import glob
from paths import dic as paths


DEBUG = True

BUTTON_CLICK_RETRY = 1 # 1 second delay between button clicks

class Scraper:
    def __init__(self, driver: webdriver.Chrome):
        driver.get(paths['target_website'])        
        self.login(driver)

    def login(self, driver: webdriver.Chrome, username: str = "", password: str = "") -> None:
        """ click on login button, enter credentials, and login user 
            @driver: instance of Driver class
            @username: username for https://www.earth2.io
            @password: password for https://www.earth2.io

            if username or password is not given, user will be input them in the terminal
        """

        if not driver.click(paths['login_btn']):
            print("[ERROR] Couldn't log in")
            return

        while not username:
            username = input("Enter username: ")

        while not password:
            password = getpass.getpass(prompt = "Enter password: ")

        driver.write(paths['username_input'], username)
        driver.write(paths['password_input'], password)


class Driver(webdriver.Chrome):
    def __init__(self, settings: str = "", *args, **kwargs):
                
        self.version = self.get_version()
        if self.version is None:
            print("[ERROR] Failed to find chromedriver, make sure to run setup.py")
            return

        self.executable_path = self.get_path()
        if self.executable_path is None:
            print("[ERROR] Failed to find chromedriver, make sure to run setup.py")
            return

        super().__init__(settings, service = Service(self.executable_path))

        # if "fullscreen" in kwargs:
        #   if kwargs["fullscreen"]:
        self.maximize_window()

        time.sleep(1)
        self.scraper = Scraper(self)

    def get_version(self) -> str:
        """ returns version of chromedriver """

        for folder in glob("./*/"):
            for file in os.listdir(folder):
                print(folder, file, file == "chromedriver")
                if file == "chromedriver":
                    return folder
            
    def get_path(self) -> str:
        """ returns executable path to chromedriver """

        exec_ending = ".exe" if sys.platform.startswith('win') else ""
        path = os.path.join(str(self.version), "chromedriver" + exec_ending)
        if os.path.isfile(path):
            return path
        return None

    def element_exists(self, xpath: str) -> bool:
        """ returns true if element exists on current page
            @xpath: xpath of element to find

        """
        for i in range(5):
            try:
                button = self.find_element(By.XPATH, xpath)
                return True
            except selenium.common.exceptions.NoSuchElementException:
                print("[ERROR] Couldn't find element {}, attempt {}".format(xpath, i + 1))

            time.sleep(1)
        return False

    def click(self, xpath: str) -> bool:
        """ click on an element 
            returns true on success
            @xpath: xpath of element to click on            
        """
        if self.element_exists(xpath):
            button = self.find_element(By.XPATH, xpath)
            button.click()
            if DEBUG:
                print("[DEBUG] Clicking on {}".format(xpath))
            return True

        return False

    def write(self, xpath: str, text: str) -> bool:
        if DEBUG:
            print("[DEBUG] Writing {} to {}".format(text, xpath))

        """ write to input 
            returns true on success
            @xpath: xpath of input
            @text: text to write
        """
        if self.element_exists(xpath):
            inpt = self.find_element(By.XPATH, xpath)
            inpt.send_keys(text)


driver = Driver({"fullscreen": True})
time.sleep(5)

# driver.quit()
