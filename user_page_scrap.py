import json
import asyncio
from pyppeteer import launch


async def scrap_user(profiles):
    user_json = []
    for url in profiles:
        try:
            # Launch a headless Chromium browser
            browser = await launch()
            page = await browser.newPage()
            
            # Navigate to the URL you want to scrape
            await page.goto(url)
        except:
            continue

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

        for each_usr in range(0,len(usernames)):
            try:
                user_row = {
                    "Username":usernames[each_usr],
                    "Short_Reviews": short_reviews[each_usr],
                    "Long_Reviews" : long_reviews[each_usr],
                    "Restaurant_names" : restaurant_names[each_usr],
                    "User_rating" : user_ratings[each_usr]
                }
                user_json.append(user_row)
            except:
                continue
    return user_json