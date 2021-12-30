from selenium import webdriver
from paths import paths
import os
from config import DEBUG

creds = {"username": "", "password": ""}

class Scraper:
    def __init__(self, driver: webdriver.Chrome):
        driver.get(paths['target_website'])        
        driver.click(paths['notice_popup'])

        # if cookies exist
        if os.path.isfile("cookies.pkl"):
            driver.load_cookies()
            driver.refresh()
            driver.click(paths['notice_popup'])
            return

        self.load_credentials()
        self.login(driver)

    def login(self, driver: webdriver.Chrome, username: str = creds['username'], password: str = creds['password']) -> None:
        if DEBUG:
            print(f"[ERROR] Logging in: {username=}, {password=}")
        """ click on login button, enter credentials, and login user 
            @driver: instance of Driver class
            @username: username for https://www.earth2.io
            @password: password for https://www.earth2.io

            if username or password is not given, user will be input them in the terminal
        """

        if not driver.click(paths['login_btn']):
            print("[ERROR] Couldn't log in")
            return

        if not 'Buy and Trade' in driver.title:
            pass
            # return 
        
        if not username or not password:
            while not driver.current_url == "https://app.earth2.io/":
                pass
            driver.click(paths['notice_popup'])
            driver.save_cookies()
            return

        driver.write(paths['username_input'], username)
        driver.write(paths['password_input'], password)

        if driver.click(paths['login_btn_continue']):
            print("Successfully logged in !!!")
        else:
            print("[ERROR] Couldn't log in")

        driver.save_cookies()
    
    def load_credentials(self):
        """ loads username and password from credentials.py """

        global creds
        try:
            from credentials import credentials
            creds = dict(credentials)
        except:
            return


