import driver
import time

driver = driver.Driver({"fullscreen": True})
driver.start()
driver.login()
driver.scrape_profile()

time.sleep(5)
