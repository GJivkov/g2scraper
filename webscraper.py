import requests
from bs4 import BeautifulSoup
from selenium import webdriver

CHROMEDRIVER_PATH = "chromedriver.exe" 
BASE_URL = "https://www.g2.com/products/trello/reviews"

driver = webdriver.Chrome(CHROMEDRIVER_PATH)
driver.implicitly_wait(5)

driver.get(BASE_URL)
page = driver.page_source

accept_cookies = driver.find_element_by_xpath('//*[@id="new_user_consent"]/input[6]').click()

html = BeautifulSoup(page, 'html.parser')

description = html.select_one('div.ws-pw p').text

print(description)

