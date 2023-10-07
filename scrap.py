

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
    
    restaurant_urls = []
    for url in urls:
        if "Restaurant_Review" in url:
            restaurant_urls.append(url)

    # Closing the browser
    await browser.close()

    restaurant_urls = list(set(restaurant_urls))
    return restaurant_urls

async def scrape_review(restaurant_urls):
    rest_name = []
    review = []
    address = []

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
       
        
        rest_name.append(r_name)
        review.append(aria_label)
        address.append(address_text)

        # Closing the browser
        await browser.close()
        break
    print(rest_name,review,address)

   

# Run the scraping function
mail_url = "https://www.tripadvisor.ca/Restaurants-g155019-Toronto_Ontario.html"
restaurant_urls = asyncio.get_event_loop().run_until_complete(scrape_website(mail_url))
asyncio.get_event_loop().run_until_complete(scrape_review(restaurant_urls))