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

    # Extract review data for the first review
    review_element = await page.querySelector('.review-container')

    # username = await page.evaluate(f'''(review_element) => {{
    #     const infoTextElement = document.querySelector('.info_text div');
    #     return infoTextElement ? infoTextElement.textContent : null;
    # }}''', review_element)



    username = await review_element.querySelectorEval('.info_text div', 'element => element.textContent.trim()')
    # username = await review_element.querySelectorEval('.info_text div > div:nth-child(1) > div:nth-child(1)', 'element => element.textContent.trim()')
    user_rating = await review_element.querySelectorEval('.ui_bubble_rating', 'element => element.getAttribute("class").match(/bubble_(\d+)/)[1]')
    review_text = await review_element.querySelectorEval('.partial_entry', 'element => element.textContent.trim()')

    # Closing the browser
    await browser.close()

    return username, user_rating, review_text

# TripAdvisor review URL
review_url = "https://www.tripadvisor.ca/Restaurant_Review-g155019-d1867454-Reviews-New_Orleans_Seafood_Steakhouse-Toronto_Ontario.html#REVIEWS"

# Scrape review data for the first user
username, user_rating, review_text = asyncio.get_event_loop().run_until_complete(scrape_review(review_url))

# Print the scraped data
print(f"Username: {username}")
print(f"User Rating: {user_rating}")
print(f"Review Text: {review_text}")
