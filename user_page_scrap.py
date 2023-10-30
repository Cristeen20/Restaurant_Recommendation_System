import json
import asyncio
from pyppeteer import launch


async def scrape_user(profiles):

    for url in profiles:
        # Launch a headless Chromium browser
        browser = await launch()
        page = await browser.newPage()
        
        # Navigate to the URL you want to scrape
        await page.goto(url)