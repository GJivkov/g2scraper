import pandas as pd
import regex as re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlparse

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
    
    if product_name is not None:
        return (product_name.find('a')['href'])
    else:
        return ("No data available")

def get_company_data(company_url):

    html = start_driver_and_get_html(company_url)

    website = html.select_one('a[itemprop$="url"]')['href']

    try:
        description = html.select_one('div[itemprop$="description"]').text
    except AttributeError:
        description = "No description available"

    try: 
        ratings = html.select_one('div[class$="text-center ai-c star-wrapper__desc__rating"]').text
        number_of_reviews = html.select_one('li[class$="list--piped__li"]').text 
    except AttributeError:
        ratings = "No ratings available"
        number_of_reviews = 0
        
    
    details_list = html.find_all("div", class_ = 'ml-1')

    details_titles = [p.next.text for p in details_list]
    
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

def get_base_url(url):
    split_url = url.split('/')
    new_url = split_url[0] + split_url[2] + '/'
    return new_url
    
companies_information = []

df = pd.read_csv('data_scientist_intern_g2_scraper.csv', encoding='utf-8')

df['NAME'].replace(r'\(.*?\)', '', regex=True, inplace=True)
df['NAME'].replace(r"^ +| +$", r"", regex=True, inplace=True) 

for ind, company in df[:30].iterrows():
    start = time.time()
    
    company_url = get_company_url(company['NAME'])
    
    if company_url != 'No data available':
        company_data = get_company_data(company_url)
            
        csv_url = urlparse(company['WEBSITE'])
        scraped_url = urlparse(company_data.get('website'))
          
        if csv_url.netloc == scraped_url.netloc:
            alternative_company_data = get_alternatives_data(company_url)
            company_data.update(alternative_company_data)
            companies_information.append(company_data)
        else:
            companies_information.append({'description': 'No match'})
    else:
        companies_information.append({'description': 'No data'})
    
    time.sleep(5)

    # As a possible measure to bypass the blocking
    if (ind + 1 % 100 == 0):
        time.sleep(600)
    
    end = time.time()
    
    print(f'Fetched {company["NAME"]} data in {(end - start):.2f}')

scraped_data = pd.DataFrame(companies_information)

scraped_data['Website'] = scraped_data['Website'].apply(lambda x: get_base_url(x) if isinstance(x, str) else x)
scraped_data[['Twitter', 'Twitter followers']] = scraped_data['Twitter'].str.split(r'(?<=[a-zA-Z])(?=[0-9])', 1, expand=True)

final_data = df.join(scraped_data)
final_data.to_csv('data_scientist_intern_g2_scraper_full.csv')