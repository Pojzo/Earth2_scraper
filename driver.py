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
import pickle
from glob import glob
from paths import paths
from scraper import Scraper
from config import DEBUG


DEBUG = True

class Driver(webdriver.Chrome):
    def __init__(self, settings: str = "", *args, **kwargs):

        exec_ending = ".exe" if sys.platform.startswith('win') else ""
        self.exec_name = "chromedriver" + exec_ending

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
                if file == self.exec_name:
                    return folder

    def get_path(self) -> str:
        """ returns executable path to chromedriver """

        path = os.path.join(str(self.version), self.exec_name)
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
            time.sleep(1)
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

    def save_cookies(self) -> None:
        """ dumps cookies to cookies.pkl """

        if DEBUG:
            print("[DEBUG] Saving cookies")

        pickle.dump(self.get_cookies(), open("cookies.pkl", "wb"))

    def load_cookies(self) -> None:
        """ loads cookies from cookies.pkl """

        if DEBUG:
            print("[DEBUG] Loading cookies")

        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            self.add_cookie(cookie)
