import pandas as pd
import regex as re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

CHROMEDRIVER_PATH = "chromedriver.exe"
QUERY_URL = "https://www.g2.com/search?utf8=%E2%9C%93&query="

def get_company_url(company):
    company = company.replace(" ", "+")
    
    full_url = QUERY_URL + company

    driver = webdriver.Chrome(CHROMEDRIVER_PATH) 
    driver.implicitly_wait(10)

    driver.get(full_url)
    page = driver.page_source

    accept_cookies = driver.find_element_by_xpath('//*[@id="new_user_consent"]/input[6]').click()

    html = BeautifulSoup(page, 'html.parser')
     
    product_name = html.select_one('div[class$="product-listing__product-name"]')
    
    if product_name is not None:
        return (product_name.find('a')['href'])
    else:
        return ("No data available")
    
    driver.quit()


df = pd.read_csv('data_scientist_intern_g2_scraper.csv', encoding='utf-8')

df['NAME'].replace(r'\(.*?\)', '', regex=True, inplace=True)
df['NAME'].replace(r"^ +| +$", r"", regex=True, inplace=True) 

def get_company_data(company_url):
    
    driver = webdriver.Chrome(CHROMEDRIVER_PATH) 
    driver.implicitly_wait(10)
    
    driver.get(company_url)
    page = driver.page_source

    accept_cookies = driver.find_element_by_xpath('//*[@id="new_user_consent"]/input[6]').click()

    html = BeautifulSoup(page, 'html.parser')

    description = html.select_one('div[itemprop$="description"]').text
    website = html.select_one('a[itemprop$="url"]')['href']

    try: 
        ratings = html.select_one('div[class$="text-center ai-c star-wrapper__desc__rating"]').text
        number_of_reviews = html.select_one('li[class$="list--piped__li"]').text 
    except AttributeError:
        ratings = "No ratings yet"
        number_of_reviews = 0
        
    
    details_list = html.find_all("div", class_ = 'ml-1')

    details_titles = [p.next.text for p in details_list] #To use as column title in Excel

    for p in details_list:
        p.find("div", class_ = 'fw-semibold').decompose()
    
    details_values = [p.text for p in details_list]

    details = dict(zip(details_titles, details_values))

    seller_details = {'description': description,
                      'website': website,
                      'number_of_reviews': number_of_reviews}

    seller_details.update(details)
    
    driver.quit()

    return seller_details

companies_information = []

for company in df['NAME'][:3]:
    company_url = get_company_url(company)
    
    print(company_url)
    
    if company_url != 'No data available':
        company_data = get_company_data(company_url)
        companies_information.append(company_data)
    else:
        companies_information.append({'description': 'No data available'})

# TODO: Optional: alternatives and pricing
# TODO: Refactoring code
# TODO: remove out of 5 stars
# TODO: remove , and reviews word