import os
import sys
try:
    print("------------------------------------")
    print("Installing requirements")
    os.system("pip install -r requirements.txt")
except:
    print("[ERROR] Pip not installed")
    sys.exit()


import chromedriver_autoinstaller
import shutil
from selenium import webdriver

print("Checking if chromedriver is installed")

chromedriver_autoinstaller.install(cwd = True)

try:
    driver = webdriver.Chrome()
    driver.get("https://www.google.com")
    print("Chromedriver is installed and should be working")
    print("------------------------------------")
except:
    print("[ERROR] Failed to install chromedriver")

print("Version of chromedriver: ", driver.capabilities['browserVersion'])
print("------------------------------------")

if not os.path.isfile("credentials.py"):
    print("credentials.py don't exist, creating")
    with open("credentials.py", "w") as file:
        string = """credentials = {
    "username": "",
    "password": ""
}"""
        file.write(string)


driver.quit()
