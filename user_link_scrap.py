import json
import asyncio
from pyppeteer import launch


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


        await page.waitForSelector('div.info_text.pointer_cursor')
        divElements = await page.querySelectorAll('div.info_text.pointer_cursor')
        
        print(review)
        for div_element in divElements:
            profile_name = await page.evaluate('(element) => element.textContent', div_element)
            
            if " " not in profile_name:
                url = "https://www.tripadvisor.ca/Profile/"+profile_name
                user_urls.append(url)

        
        await browser.close()
        

    return user_urls

# Run the scraping function
main_url = "https://www.tripadvisor.ca/Restaurants-g155019-Toronto_Ontario.html#REVIEWS"
review_urls = asyncio.get_event_loop().run_until_complete(scrape_website(main_url))
profile_urls = asyncio.get_event_loop().run_until_complete(user_scrap(review_urls))
