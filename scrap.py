
import json
import asyncio
from pyppeteer import launch

from restaurant_review import scrape_review
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
    
    restaurant_urls = []
    for url in urls:
        if "Restaurant_Review" in url and "#REVIEWS" not in url:
            restaurant_urls.append(url)

    # Closing the browser
    await browser.close()

    restaurant_urls = list(set(restaurant_urls))
    print(restaurant_urls)
    return restaurant_urls

async def scrape_restaurant(restaurant_urls):
    rest_json = []

    for restaurant in restaurant_urls:
        # Launch a headless Chromium browser
        print(restaurant)
        browser = await launch()
        # Create a new page/tab
        page = await browser.newPage()
        
        # Navigate to the URL you want to scrape
        await page.goto(restaurant)

        class_name = "HjBfq"        
        r_name = await page.evaluate(f'''(class_name) => {{
        const h1 = document.querySelector('h1.{class_name}');
        return h1 ? h1.textContent : null;
        }}''', class_name)
        print(r_name)

        class_name = "UctUV d H0"
        aria_label = await page.evaluate('''() => {
        const svgElement = document.querySelector('svg[aria-label]');
        return svgElement ? svgElement.getAttribute('aria-label') : null;
        }''')
        print(aria_label)

        
        await page.waitForSelector('a.AYHFM')
        divElements = await page.querySelectorAll('a.AYHFM')
        address_text = await page.evaluate('(element) => element.textContent', divElements[1])

        rest_cusine = []
        await page.waitForSelector('a.dlMOJ')
        divElements = await page.querySelectorAll('a.dlMOJ')
        for cus in divElements[1:]:
            cusine_type = await page.evaluate('(element) => element.textContent', cus)
            rest_cusine.append(cusine_type)

        await page.waitForSelector('span.AfQtZ')
        divElement = await page.querySelector('span.AfQtZ')
        review_num = await page.evaluate('(element) => element.textContent', divElement)

        await browser.close()

        review_url = restaurant+"#REVIEWS"
        review_texts = await asyncio.create_task(scrape_review(review_url))
        restaurant_scrap_row = {"Restaurant Name":r_name,
                                "Rating":aria_label,
                                "Address":address_text,
                                "Cusines":rest_cusine,
                                "Review Count":review_num,
                                "Review List":review_texts
                                }
        
        rest_json.append(restaurant_scrap_row)

        
        
        
    return rest_json

   

# Run the scraping function
#https://www.tripadvisor.ca/Restaurants-g181740-Richmond_Hill_Ontario.html
#https://www.tripadvisor.ca/Restaurants-g155019-Toronto_Ontario.html
main_url = "https://www.tripadvisor.ca/Restaurants-g181720-Markham_Ontario.html"
restaurant_urls = asyncio.get_event_loop().run_until_complete(scrape_website(main_url))
rest_json = asyncio.get_event_loop().run_until_complete(scrape_restaurant(restaurant_urls))
write_csv(rest_json,"Restaurant_data.csv")
