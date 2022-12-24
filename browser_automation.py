from pyppeteer import launch
import asyncio

# url for getting the list of IPOs listed on NSE in 2022
url = 'https://www1.nseindia.com/products/content/equities/ipos/hist_ipo.htm'

async def url_content(url):
    '''
    This function automates the browser for a apecified url and returns the page source 
    '''
    browser = await launch({"headless":False,'args':['--start-maximized']})
    page = await browser.newPage()
    await page.goto(url)
    await asyncio.sleep(5)
    page_content = await page.content()
    await browser.close()
    return page_content

page_source = asyncio.get_event_loop().run_until_complete(url_content(url))