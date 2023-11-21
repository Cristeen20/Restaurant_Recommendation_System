import asyncio
from pyppeteer import launch


async def scrape_review(review_url):
    # Launch a headless Chromium browser
    browser = await launch()
    # Create a new page/tab
    page = await browser.newPage()
    
    # Navigate to the URL you want to scrape
    await page.goto(review_url)

    # Wait for the review section to load (you may need to adjust this selector)
    await page.waitForSelector('.review-container')

    # Extract review data for multiple reviews
    review_elements = await page.querySelectorAll('.review-container')

    review_texts = []

    for review_element in review_elements:
        #username = await review_element.querySelectorEval('.info_text div', 'element => element.textContent.trim()')
        #user_rating = await review_element.querySelectorEval('.ui_bubble_rating', 'element => element.getAttribute("class").match(/bubble_(\d+)/)[1]')
        review_text = await review_element.querySelectorEval('.partial_entry', 'element => element.textContent.trim()')

        review_texts.append(review_text)

    # Closing the browser
    await browser.close()

    return review_texts






