## Important

Because we use webdriver for the scraping, it is crucial for the user to have the correct driver when using the script. The driver has to be put in the same folder, replacing the driver I used. I used Chrome driver 92 version, which can be downloaded here: https://chromedriver.chromium.org/downloads

Another type of driver can be used, such as Mozzila Firefox, Edge and etc.

## Things to improve:
- I did not add any testing and my exception handling is down to the minimum (just because this is a task focused on the scraping part)
- Webdriver version and type. Currently, it requires from the user to do things manually, but a nice functionality will be to check and download automatically the proper driver.
- CSV export. At the moment, it just merges the two dataframes and exports to a new csv. I thought that this is a better solution than appending to an already existing csv, as it might be problematic.
- Time complexity. At the moment, it takes around 5 (10 with added time.sleep(5)) seconds to get information for a company that has no data, 10(15sec) to get information about a company that had some search results, but it didn't match the company urls, and around 18(23seconds) to get company information when there was a match.
- Related to the previous point, I also assumed that the top search results is the only possible match for the company. This, of course, is a very naive assumption given that a company name can be very generic. I did go through a few possible companies and decided that the added time for this functionality is something to be discussed before implementing.
- Twitter handles: I assumed that the twitter handles won't have numbers in them (don't know if that is the case), so my regex splits on the first number occurance.
- Add DOCSTRINGS for the functions.
- Data cleaning: Something to be discussed, but I could have removed things such as 'reviews', 'twitter followers' and etc.

## Problems that occured:
- I originally tried doing this task with requests and beautifulsoup4 only, but there were many issues that were easily solved with the use of selenium.
- Cookies
- hCaptcha blocking. This is the biggest problem for the webscraper. Currently, it stops the script execution by throwing a NoSuchElementException (for the cookies). I don't think that there is a easy solution for this (I did add a few time.sleeps and I managed to scrape around 250 companies before I got blocked. The scraped data is [data_scientist_intern_g2_scraper_full.csv](../blob/master/data_scientist_intern_g2_scraper_full.csv)
- A lot of missing data: I thought that this is weird, but I checked manually for a few random companies and I also couldn't find information about them.

## Going through the code logic:
