## Important

Because we use webdriver for the scraping, it is crucial for the user to have the correct driver when using the script. The driver has to be put in the same folder, replacing the driver I used. I used Chrome driver 92 version, which can be downloaded here: https://chromedriver.chromium.org/downloads

Another type of driver can be used, such as Mozzila Firefox, Edge and etc.

---
## Going through the code:

In [webscraper.py](../blob/master/webscraper.py) you can find all of the code. 

It starts with imports of:
* pandas ([docs](https://pandas.pydata.org/docs/))
* regex ([docs](https://docs.python.org/3/library/re.html))
* time ([docs](https://docs.python.org/3/library/time.html))
* beautifulsoup ([docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/))
* selenium ([docs](https://selenium-python.readthedocs.io/))
* urlparse ([docs](https://docs.python.org/3/library/urllib.parse.html))

It consists of 5 functions:

+ start_driver_and_get_html(url) - Initialize the webdriver, load the page, extract the html source, accept cookies, parse the html, close driver and returns html.
+ get_company_url(company) - Replace spaces in company name with '+' (to work for the query url), make up the full url and extract hyperlink of the company (g2 site url)
+ get_company_data(company_url) - Extract company website, description, ratings, number of reviews, product and seller details and returns dictionary with everything available.
+ get_alternatives_data(company_url) - Gather alternative companies (top 20)
+ get_base_url(url) - Extract base url in order to compare later on.

We load the csv data, then we remove brackets (and everything inside them) from the company names, we remove the empty space at the end. Then, we start iterating over the companies 1 by 1, for each iteration we start a timer, extract company url - if there is no data, append "No data" and go to the next company, otherwise if there is data, we check if the company website matches the scraped company website. If there is a match, we scrape the alternatives and update the company data, otherwise we append "No match". We stop the timer and print how much time it took. After we collect the data, we store only the base url (because some website have more specific urls provided) and we split the twitter data into 2 columns Twitter (handle) and Twitter followers.

---
## Things to improve:
- I did not add any testing and my exception handling is down to the minimum (just because this is a task focused on the scraping part)
- Webdriver version and type. Currently, it requires from the user to do things manually, but a nice functionality will be to check and download automatically the proper driver.
- CSV export. At the moment, it just merges the two dataframes and exports to a new csv. I thought that this is a better solution than appending to an already existing csv, because it is not as straightforward (for example with openpyxl
- Time complexity. At the moment, it takes around 5 (10 with added time.sleep(5)) seconds to get information for a company that has no data, 10(15sec) to get information about a company that had some search results, but it didn't match the company urls, and around 18(23seconds) to get company information when there was a match.
- Related to the previous point, I also assumed that the top search results is the only possible match for the company. This, of course, is a very naive assumption given that a company name can be very generic. I did go through a few possible companies and decided that the added time for this functionality is something to be discussed before implementing.
- Twitter handles: I assumed that the twitter handles won't have numbers in them (don't know if that is the case), so my regex splits on the first number occurance.
- Add DOCSTRINGS for the functions.
- Data cleaning: Something to be discussed, but I could have removed things such as 'reviews', 'twitter followers' and etc.

---
## Problems that occured:
- I originally tried doing this task with requests and beautifulsoup4 only, but there were many issues that were easily solved with the use of selenium.
- Cookies
- hCaptcha blocking. This is the biggest problem for the webscraper. Currently, it stops the script execution by throwing a NoSuchElementException (for the cookies). I don't think that there is a easy solution for this (I did add a few time.sleeps and I managed to scrape around 250 companies before I got blocked. The scraped data is [data_scientist_intern_g2_scraper_full.csv](../blob/master/data_scientist_intern_g2_scraper_full.csv)
- A lot of missing data: I thought that this is weird, but I checked manually for a few random companies and I also couldn't find information about them.

---
### NOTES

Currently the scraper goes through only 30 companies. If you need that changed, either change the number for the slicing or remove it altogether.

I didn't scrape "Pricing", because when I try to open it with the webdriver I get instantly blocked, so I can't check if it works. Otherwise the implementation seems pretty straightforward.

I am not sure if the 'description' I scraped is the correct one.
