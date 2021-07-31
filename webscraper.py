import pandas as pd
import regex as re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

CHROMEDRIVER_PATH = "chromedriver.exe"
QUERY_URL = "https://www.g2.com/search?utf8=%E2%9C%93&query="

def start_driver_and_get_html(url):

    driver = webdriver.Chrome(CHROMEDRIVER_PATH) 
    driver.implicitly_wait(10)
    
    driver.get(url)
    page = driver.page_source

    driver.find_element_by_xpath('//*[@id="new_user_consent"]/input[6]').click()

    html = BeautifulSoup(page, 'html.parser')

    driver.quit()

    return html

def get_company_url(company):
    company = company.replace(" ", "+")
    
    full_url = QUERY_URL + company

    html = start_driver_and_get_html(full_url)
     
    product_name = html.select_one('div[class$="product-listing__product-name"]')
    print(product_name)
    
    if product_name is not None:
        return (product_name.find('a')['href'])
    else:
        return ("No data available")


def get_company_data(company_url):

    html = start_driver_and_get_html(company_url)

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
    
    details_values = []
    
    for p in details_list:
        
        p.find("div", class_ = 'fw-semibold').decompose()
        link = p.find("a", class_ = 'link')
    
        if link is not None:
            p = link['href']
        else:
            p = p.text
    
        details_values.append(p)

    details = dict(zip(details_titles, details_values))

    seller_details = {'description': description,
                      'website': website,
                      'ratings': ratings,
                      'number_of_reviews': number_of_reviews}

    seller_details.update(details)
    
    return seller_details

def get_alternatives_data(company_url):

    company_url_alternatives = company_url.replace('reviews', 'competitors/alternatives')
    
    html = start_driver_and_get_html(company_url_alternatives)
    
    alternatives = html.select('div[itemprop$="name"]')
    alternative_companies = [alt_company.text for alt_company in alternatives]
    
    return {'alternative_companies': ', '.join(alternative_companies)}
    

companies_information = []

df = pd.read_csv('data_scientist_intern_g2_scraper.csv', encoding='utf-8')

df['NAME'].replace(r'\(.*?\)', '', regex=True, inplace=True)
df['NAME'].replace(r"^ +| +$", r"", regex=True, inplace=True) 

for company in df['NAME'][:5]:

    print(f'Fetching {company} data')

    company_url = get_company_url(company)

    if company_url != 'No data available':
        company_data = get_company_data(company_url)
        alternative_company_data = get_alternatives_data(company_url)
        
        company_data.update(alternative_company_data)
        companies_information.append(company_data)
    else:
        companies_information.append({'description': 'No data'})

# TODO: Optional: alternatives and pricing