from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
from time import sleep
import requests

def get_html(url):
    
    html_content = ''
    try:
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_content = BeautifulSoup(page.content, "html.parser")
    except: 
        pass
    
    return html_content

def get_details(url):
    
    stamp = {}
    
    try:
        html = get_html(url)
    except:
        return stamp

    try:
        price = html.select('.product-details__price')[0].get_text().strip()
        stamp['price'] = price.replace('£', '').replace(',', '').strip()
    except: 
        stamp['price'] = None
        
    try:
        title = html.select('.store-product-name')[0].get_text().strip()
        stamp['title'] = title
    except:
        stamp['title'] = None
        
    try:
        stock_num = html.select('[itemprop=sku]')[0].get("content")
        stamp['stock_num'] = stock_num
    except:
        stamp['stock_num'] = None    
        
    try:
        selection = html.select('.breadcrumbs')[0].get_text().strip()
        selection = selection.replace('\n', ' / ')
        stamp['selection'] = selection
    except:
        stamp['selection'] = None 
        

    stamp['currency'] = "GBP"

    # image_urls should be a list
    images = []                    
    try:
        image_items = html.select('.product-details__image > img')
        for image_item in image_items:
            img = image_item.get('src')
            if img not in images:
                images.append(img)
    except:
        pass
    
    stamp['image_urls'] = images 
    
    try:
        raw_text = html.select('.product-details__description')[0].get_text().strip()
        stamp['raw_text'] = raw_text
    except:
        stamp['raw_text'] = None
        
    if stamp['raw_text'] == None and stamp['title'] != None:
        stamp['raw_text'] = stamp['title']

    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date

    stamp['url'] = url
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
           
    return stamp

def get_page_items(url):

    items = []

    try:
        html = get_html(url)
    except:
        return items, next_url

    try:
        for item in html.select('.card__content a'):
            item_link = 'https://www.stanleygibbons.com' + item.get('href')
            if item_link not in items:
                items.append(item_link)
    except:
        pass

    shuffle(list(set(items)))
    
    return items

def get_last_page(url):

    page_numbers = []

    try:
        html = get_html(url)
    except:
        return last_page

    try:
        last_page = html.select('.pagination a')[-2].get_text()
        last_page = int(last_page)
    except:
        pass
    
    if last_page:
        for page_number in range(1, last_page):    
            page_numbers.append(page_number)
        shuffle(page_numbers)
    
    return page_numbers

categories = {"great britain stamps":"https://www.stanleygibbons.com/shop/great-britain-stamps","commonwealth world":"https://www.stanleygibbons.com/shop/commonwealth-world-stamps?commonwealth_stamp_region=Africa&sort=name%7Casc"}
for category_name in categories:
    print(category_name + ': ' + categories[category_name])   

selected_category_name = input('Choose category: ')
selected_category = categories[selected_category_name]
page_numbers = get_last_page(selected_category)
for page_number in page_numbers:
    page_url = selected_category
    if '?' in selected_category:
        page_url += '&'
    else:
        page_url += '?'
    page_url += 'ccm_paging_p=' + str(page_number) 
    page_items = get_page_items(page_url)
    for page_item in page_items:
            stamp = get_details(page_item)
