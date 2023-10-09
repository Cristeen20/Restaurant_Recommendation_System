import asyncio
from pyppeteer import launch

async def scrape_reviews(review_url, num_reviews=5):
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

    usernames = []
    user_ratings = []
    review_texts = []

    for review_element in review_elements[:num_reviews]:
        username = await review_element.querySelectorEval('.info_text div', 'element => element.textContent.trim()')
        user_rating = await review_element.querySelectorEval('.ui_bubble_rating', 'element => element.getAttribute("class").match(/bubble_(\d+)/)[1]')
        review_text = await review_element.querySelectorEval('.partial_entry', 'element => element.textContent.trim()')

        usernames.append(username)
        user_ratings.append(user_rating)
        review_texts.append(review_text)

    # Closing the browser
    await browser.close()

    return usernames, user_ratings, review_texts

# TripAdvisor review URL
review_url = "https://www.tripadvisor.ca/Restaurant_Review-g155019-d1867454-Reviews-New_Orleans_Seafood_Steakhouse-Toronto_Ontario.html#REVIEWS"

# Scrape data for 5 user reviews
usernames, user_ratings, review_texts = asyncio.get_event_loop().run_until_complete(scrape_reviews(review_url, num_reviews=5))

# Print the scraped data
for i in range(len(usernames)):
    print(f"User {i+1} - Username: {usernames[i]}")
    print(f"User {i+1} - User Rating: {user_ratings[i]}")
    print(f"User {i+1} - Review Text: {review_texts[i]}\n")
