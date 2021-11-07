import argparse
import requests
from bs4 import BeautifulSoup
import json
import csv

def parse_itemssold(text):
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'sold' in text:
        return int(numbers)
    else:
        return 0

def parse_price(text):
    numbers = ''
    cents = 0
    for char in text:
        if char in '$0123456789.,+':
            numbers += char
        else:
            break
    if 'free' in text.lower():
        return 0
    else:
        if len(numbers) > 0:
            numbers = numbers.replace('$','')
            numbers = numbers.replace('.','')
            numbers = numbers.replace(',','')
            numbers = numbers.replace('+','')
            cents = int(numbers)
        return cents

if __name__ == '__main__':
    # process command line args
    parser = argparse.ArgumentParser(description='Download info from eBay and convert to JSON.')
    parser.add_argument('search_term')
    parser.add_argument('--num_pages', default=10)
    parser.add_argument('--csv', action='store_true')
    args = parser.parse_args() 
    items = [] #took me a while to realize that this should go BEFORE the for-loop. Thanks for the help, Chuck!

    for page_number in range(1, (args.num_pages + 1)): #urls for search pages 1 to 10
        
        #build the url
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw='
        url += (args.search_term).replace(' ', '+')
        url += '&_sacat=0&LH_TitleDesc0&_pgn='
        url += str(page_number)
        url += '&rt=nc'
        
        #download the html
        r = requests.get(url)
        status = r.status_code
        html = r.text
        
        #process the html
        soup = BeautifulSoup(html, 'html.parser')
        tags_items = soup.select('.s-item')
        
        for tag_item in tags_items:
            name = None
            tags_name = tag_item.select('.s-item__title')
            for tag in tags_name:
                name = tag.text

            price = None
            tags_price = tag_item.select('.s-item__price')
            for tag in tags_price:
                price = parse_price(tag.text)

            status = None
            tags_status = tag_item.select('.s-item__subtitle') #'SECONDARY_INFO'
            for tag in tags_status:
                status = tag.text

            shipping = None
            tags_shipping = tag_item.select('.s-item__logisticsCost')
            for tag in tags_shipping:
                shipping = parse_price(tag.text)

            freereturns = False
            tags_freereturns = tag_item.select('.s-item__free-returns')
            for tag in tags_freereturns:
                freereturns = True

            items_sold = None
            tags_itemssold = tag_item.select('.s-item__hotness')
            for tag in tags_itemssold:
                items_sold = parse_itemssold(tag.text)

            item = ({ #creates dictionary for each tag
                'name' : name,
                'price' : price,
                'status' : status,
                'shipping' : shipping,
                'free_returns' : freereturns,
                'items_sold' : items_sold
            })
            items.append(item)

if args.csv:
    keys = items[0].keys()
    with open(args.search_term+'.csv', 'w', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(items)

else:
    filename = args.search_term+'.json'
    with open(filename, 'w', encoding = 'ascii') as f:
        f.write(json.dumps(items))