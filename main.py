from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
from glob import glob

class Driver(webdriver.Chrome):
    def __init__(self, settings: str = ""):
        self.version = self.get_version()
        if self.version is None:
            print("[ERROR] Failed to find chromedriver, make sure to run setup.py")
            return

        self.executable_path = self.get_path()
        if self.executable_path is None:
            print("[ERROR] Failed to find chromedriver, make sure to run setup.py")
            return

        super().__init__(settings, service = Service(self.executable_path))

    def get_version(self):
        """ returns version of chromedriver """
        for folder in glob("./*/"):
            for file in os.listdir(folder):
                print(folder, file, file == "chromedriver")
                if file == "chromedriver":
                    return folder
            
    def get_path(self):
        """ returns executable path to chromedriver """
        path = os.path.join(str(self.version), "chromedriver")
        if os.path.isfile(path):
            return path
        return None

    
    def test(self):
        self.get("https://www.google.com")

driver = Driver()
driver.get("https://www.google.com")


