
import asyncio
import csv
from pyppeteer import launch

async def scrape_restaurant_data(restaurant_url):
    # Launch a headless Chromium browser
    browser = await launch()
    page = await browser.newPage()
    
    try:
        # Navigate to the restaurant URL
        await page.goto(restaurant_url)
        
        # Extract restaurant information
        class_name = "HjBfq"        
        restaurant_name = await page.evaluate(f'''(class_name) => {{
            const h1 = document.querySelector('h1.{class_name}');
            return h1 ? h1.textContent : null;
        }}''', class_name)

        class_name = "UctUV d H0"
        restaurant_rating = await page.evaluate('''() => {
            const svgElement = document.querySelector('svg[aria-label]');
            return svgElement ? svgElement.getAttribute('aria-label') : null;
        }''')

        await page.waitForSelector('a.AYHFM')
        divElements = await page.querySelectorAll('a.AYHFM')
        restaurant_address = await page.evaluate('(element) => element.textContent', divElements[1])
        
        # Scrape user reviews
        review_url = f"{restaurant_url}#REVIEWS"
        await page.goto(review_url)
        await page.waitForSelector('.review-container')
        
        user_reviews = []
        review_elements = await page.querySelectorAll('.review-container')
        
        for review_element in review_elements:
            review_text = await review_element.querySelectorEval('.partial_entry', 'element => element.textContent.trim()')
            
            user_reviews.append(review_text)
        
        # Closing the browser
        await browser.close()

        # Construct and return the data
        restaurant_data = {
            'Restaurant Name': restaurant_name,
            'Restaurant Rating': restaurant_rating,
            'Restaurant Address': restaurant_address,
            'User Reviews': user_reviews
        }

        return restaurant_data
    except Exception as e:
        print(f"Error scraping restaurant data: {str(e)}")
        return None

async def main():
    restaurant_url = "https://www.tripadvisor.ca/Restaurant_Review-g155019-d1867454-Reviews-New_Orleans_Seafood_Steakhouse-Toronto_Ontario.html"
    
    restaurant_data = await scrape_restaurant_data(restaurant_url)

    if restaurant_data:
        # Save data to CSV file
        with open('restaurant_data.csv', mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['Restaurant Name', 'Restaurant Rating', 'Restaurant Address', 'User Reviews']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
            # Write header row
            writer.writeheader()
            
            # Write restaurant data with all review text as a list
            writer.writerow({
                'Restaurant Name': restaurant_data['Restaurant Name'],
                'Restaurant Rating': restaurant_data['Restaurant Rating'],
                'Restaurant Address': restaurant_data['Restaurant Address'],
                'User Reviews': "\n".join(restaurant_data['User Reviews'])  # Combine all reviews into one string
            })
        print("Data saved to restaurant_data.csv")

    else:
        print("Failed to scrape restaurant data.")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())


