from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHROMEDRIVER_PATH = "chromedriver.exe" 
BASE_URL = "https://www.g2.com/products/trello/reviews"

driver = webdriver.Chrome(CHROMEDRIVER_PATH) 
driver.implicitly_wait(10)

driver.get(BASE_URL)
page = driver.page_source

accept_cookies = driver.find_element_by_xpath('//*[@id="new_user_consent"]/input[6]').click()

html = BeautifulSoup(page, 'html.parser')

description = html.select_one('div[itemprop$="description"]').text
website = html.select_one('a[itemprop$="url"]')['href']

# TODO: remove out of 5 stars
ratings = html.select_one('div[class$="text-center ai-c star-wrapper__desc__rating"]').text

# TODO: remove , and reviews word
number_of_reviews = html.select_one('li[class$="list--piped__li"]').text 


product_seller_details = html.find_all()

# TODO: Optional: alternatives and pricing



print(website)
print(ratings)
print(number_of_reviews)