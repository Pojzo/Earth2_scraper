import chromedriver_autoinstaller
from selenium import webdriver

print("Checking if chromedriver is installed")

chromedriver_autoinstaller.install()

try:
    driver = webdriver.Chrome()
    driver.get("https://www.google.com")
    print("Chromedriver is installed and should be working")
except:
    print("[ERROR] Failed to install chromedriver")

driver.quit()
