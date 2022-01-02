from selenium import webdriver
import snoop
from selenium.webdriver.common.by import By
from paths import paths
from e2_property import Property
import os
import time
from config import DEBUG


class Credentials:
    def __init__(self):
        try:
            from credentials import credentials
            self.creds = dict(credentials)
        except:
            self.creds = {"username": "", "password": ""}


class Scraper:
    def __init__(self, driver: webdriver.Chrome):
        self.credentials = Credentials()
        self.logged_in = False
        self.properties = []

    def start(self, driver: webdriver.Chrome):
        """ load target website, load cookies and login
            @driver: instance of Driver class
        """

        driver.get(paths['links']['target_website'])
        driver.click(paths['notice_popup'])

        if os.path.isfile("cookies.pkl"):
            driver.load_cookies()
            driver.refresh()
            driver.get(paths['links']['profile_link'])
            driver.click(paths['notice_popup'])
            self.logged_in = True
            return

    def login(self, driver: webdriver.Chrome) -> None:

        """ click on login button, enter credentials, and login user
            @driver: instance of Driver class
        """

        if self.logged_in:
            print("Already logged in")
            return

        username = self.credentials.creds['username']
        password = self.credentials.creds['password']

        if DEBUG:
            print(f"[DEBUG] Logging in: {username=}, {password=}")

        if not driver.click(paths['login_btn']):
            print("[ERROR] Couldn't log in")
            return

        if 'Buy and Trade' not in driver.title:
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
        driver.click(paths['notice_popup'])

    def scrape_profile(self, driver: webdriver.Chrome) -> None:
        property_links = []
        index = 0
        while True:
            try:
                index += 1
                property_links.append(driver.get_href(
                    paths['profile']['property_link'].format(index)))
                print(f"Property number {index}: {property_links[-1]}")
            except Exception as e:
                if False:  # xddd
                    print(e)
                break
