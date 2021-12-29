import os
import sys
try:
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

print(driver.capabilities['browserVersion'])

# version = str(driver.capabilities['browserVersion']).split('.')[0]
# os.rename(f"{version}/chromedriver", "chromedriver")
# hutil.rmtree(version)

# install requirements
print("------------------------------------")
print("Installing requirements")

driver.quit()
