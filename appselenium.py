# app.py

import os
import json
import time

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def doScraping(billerCode):
    # driver = webdriver.Chrome("./chromedriver")
    driver = webdriver.Firefox()

    bpayURL = "https://bpay.com.au/BillerLookupResults?query={billerCode}".format(billerCode=billerCode)
    driver.get(bpayURL)

    print(driver.title)
    time.sleep(3)

    inputxp = '//*[@id="query"]'
    inputTB = driver.find_element_by_xpath(inputxp)
    inputTB.clear()
    inputTB.send_keys("75556")
    inputTB.send_keys(Keys.ENTER)

    time.sleep(5)
    longnamexp = '//*[@id="tab1"]/div/div/div[1]/div[1]/h3'
    longname = driver.find_element_by_xpath(longnamexp)

    print('longname={}'.format(longname.text))

    xp = '//*[@id="tab1"]/div/div/div[1]/div[2]/div/div[1]/p[2]'
    billerCodeXP = driver.find_element_by_xpath(xp)
    print(billerCodeXP.get_attribute('innerHTML'))

    driver.close()

    return "done"


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("eg. python app.py billerCode")
        sys.exit(1)
        
    billerCode = sys.argv[1]

    res = doScraping(billerCode)

    print(res)
