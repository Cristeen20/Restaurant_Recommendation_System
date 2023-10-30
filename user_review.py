import asyncio
from pyppeteer import launch

async def scrape_reviews(profile_url):
    # Launch a headless Chromium browser
    browser = await launch()

    # Create a new page/tab
    page = await browser.newPage()

    # Navigate to the TripAdvisor profile URL
    await page.goto(profile_url)

    # Wait for the elements to load
    await page.waitForSelector('.ui_link.uyyBf')
    await page.waitForSelector('.AzIrY.b._a.VrCoN')
    await page.waitForSelector('q.BTPVX')
    await page.waitForSelector('.Jkczm.b.W.o.q.ui_link[title]')
    await page.waitForSelector('span.ui_bubble_rating')

    # Extract the usernames
    usernames = await page.evaluate('''() => {
        const usernameElements = document.querySelectorAll('.ui_link.uyyBf');
        return Array.from(usernameElements).map(element => element.textContent);
    }''')

    # Extract short reviews with the class '.AzIrY.b._a.VrCoN'
    short_reviews = await page.evaluate('''() => {
        const shortReviewElements = document.querySelectorAll('.AzIrY.b._a.VrCoN');
        return Array.from(shortReviewElements).map(element => element.textContent);
    }''')

    # Extract long reviews enclosed in <q class="BTPVX"></q>
    long_reviews = await page.evaluate('''() => {
        const longReviewElements = document.querySelectorAll('q.BTPVX');
        return Array.from(longReviewElements).map(element => element.textContent);
    }''')

    # Extract restaurant names
    restaurant_names = await page.evaluate('''() => {
        const restaurantNameElements = document.querySelectorAll('.Jkczm.b.W.o.q.ui_link[title]');
        return Array.from(restaurantNameElements).map(element => element.textContent);
    }''')

    # Extract user ratings
    user_ratings = await page.evaluate('''() => {
        const ratingElements = document.querySelectorAll('.muQub.VrCoN span.ui_bubble_rating');
        return Array.from(ratingElements).map(element => element.className);
    }''')

    # Closing the browser
    await browser.close()

    return usernames, short_reviews, long_reviews, restaurant_names, user_ratings

# URL of the TripAdvisor profile to scrape
profile_url = "https://www.tripadvisor.ca/Profile/LD100Toronto?fid=83c505c8-9c4c-4f64-b31f-badaea8c644f"

# Run the scraping function for the profile URL
usernames, short_reviews, long_reviews, restaurant_names, user_ratings = asyncio.get_event_loop().run_until_complete(scrape_reviews(profile_url))

# Print the extracted information
for i in range(len(usernames)):
    print("Username:", usernames[i])
    print("Short Review:", short_reviews[i])
    print("Long Review:", long_reviews[i])
    print("Restaurant Name:", restaurant_names[i])
    print("User Rating:", user_ratings[i])
    print()

