from selenium import webdriver
from selenium.webdriver.common.by import By
from paths import paths
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
        driver.click(paths['notice_popup'])
    
    def scrape_profile(self, driver: webdriver.Chrome) -> None:
        driver.get(paths['links']['profile_link'])
        print("I am here waiting 5 seconds")
        time.sleep(5)
        index = 1
        while True:
            name_xpath = paths['profile']['property_name'].format(index)
            net_worth_xpath = paths['profile']['property_net_worth'].format(index)
            coordinates_xpath = paths['profile']['property_coordinates'].format(index)
            location_xpath = paths['profile']['property_location'].format(index)

            # print(name_xpath)
            # print(net_worth_xpath)
            # print(coordinates_xpath)
            # print(location_xpath)

            try:
                name = driver.find_element(By.XPATH, name_xpath)
                net_worth = driver.find_element(By.XPATH, net_worth_xpath)
                coodinates = driver.find_element(By.XPATH, coordinates_xpath)
                location = driver.find_element(By.XPATH, location_xpath)
            except:
                break

            print(name.text)
            print(net_worth.text)
            print(coodinates.text)
            print(location.text)
            index += 1
            
        print(f"Found {index} ")
        time.sleep(1)

