import json
import asyncio
from pyppeteer import launch

from user_page_scrap import scrap_user
from csv_write import write_csv

async def scrape_website(url):

    # Launch a headless Chromium browser
    browser = await launch()
    page = await browser.newPage()
    
    # Navigate to the URL you want to scrape
    await page.goto(url)

    urls = await page.evaluate('''() => {
        const links = Array.from(document.querySelectorAll('a'));
        return links.map(link => link.href);
    }''')
    
    review_urls = []
    for url in urls:
        if "#REVIEWS" in url:
            review_urls.append(url) 

    # Closing the browser
    await browser.close()

    return review_urls

async def user_scrap(review_urls):
    user_urls = []
    for review in review_urls:
        # Launch a headless Chromium browser
        browser = await launch()
        # Create a new page/tab
        page = await browser.newPage()
        
        # Navigate to the URL you want to scrape
        await page.goto(review)

        user_div_name = 'ui_avatar.resp'
        await page.waitForSelector(f'div.{user_div_name}')
    
        await page.click(f'div.{user_div_name}')
        await page.waitForSelector('div.memberOverlayRedesign.g10n')
        user_div = await page.querySelector('div.memberOverlayRedesign.g10n')
        user_href = await user_div.querySelector('a')
        url = await page.evaluate('(element) => element.getAttribute("href")', user_href)

        print(url)
        user_url = 'https://www.tripadvisor.ca' + url
        user_urls.append(user_url)

        await browser.close()
        
        

    return user_urls

# Run the scraping function
#https://www.tripadvisor.ca/Restaurants-g155019-Toronto_Ontario.html
#https://www.tripadvisor.ca/Restaurants-g181740-Richmond_Hill_Ontario.html
main_url = "https://www.tripadvisor.ca/Restaurants-g181720-Markham_Ontario.html#REVIEWS"
review_urls = asyncio.get_event_loop().run_until_complete(scrape_website(main_url))
profile_urls = asyncio.get_event_loop().run_until_complete(user_scrap(review_urls))
user_json = asyncio.get_event_loop().run_until_complete(scrap_user(profile_urls))
write_csv(user_json,"User_data.csv")