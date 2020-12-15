import json
from bs4 import BeautifulSoup
from helium import *
import requests
import time
import re
import csv

amazon_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip',
    'DNT': '1',  # Do Not Track Request Header
    'Connection': 'close',
    'referer': 'https://www.amazon.com/'
}


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip',
    'DNT': '1',  # Do Not Track Request Header
    'Connection': 'close',
}

# urls = [
#     'https://www.penguinrandomhouse.com/ajaxc/categories/books/?from=0&to=101&contentId=business&elClass=book&dataType=html&catFilter=all&sortType=frontlistiest_onsale',
#     'https://www.penguinrandomhouse.com/ajaxc/categories/books/?from=100&to=201&contentId=business&elClass=book&dataType=html&catFilter=all&sortType=frontlistiest_onsale',
#     'https://www.penguinrandomhouse.com/ajaxc/categories/books/?from=200&to=301&contentId=business&elClass=book&dataType=html&catFilter=all&sortType=frontlistiest_onsale',
# ]
urls = 'https://www.penguinrandomhouse.com/ajaxc/categories/books/?from=0&to=4344&contentId=business&elClass=book&dataType=html&catFilter=all&sortType=frontlistiest_onsale',

for url in urls:
    response = requests.get(url, headers=headers)
    s = BeautifulSoup(response.content, features='lxml')
    increment = int(0)
    while (increment < 101):
        title = '-'
        author = '-'
        isbn = '-'
        category = '-'
        pages = '-'
        release_date = '-'
        paperback = '-'
        hardcover = '-'
        rating = '-'
        stars = '-'
        cover = '-'
        amazon = '-'
        try:
            result = s.select(f'body > div:nth-child({increment}) > div.title > a')[
                0]
            try:
                author3 = s.select(f'body > div:nth-child({increment}) > div.contributor > a:nth-child(3)')[
                    0].get_text().strip()
                author2 = s.select(f'body > div:nth-child({increment}) > div.contributor > a:nth-child(2)')[
                    0].get_text().strip()
                author = s.select(f'body > div:nth-child({increment}) > div.contributor > a:nth-child(1)')[
                    0].get_text().strip()
                author = f'{author}, {author2}, {author3}'
            except:
                try:
                    author2 = s.select(f'body > div:nth-child({increment}) > div.contributor > a:nth-child(2)')[
                        0].get_text().strip()
                    author = s.select(f'body > div:nth-child({increment}) > div.contributor > a:nth-child(1)')[
                        0].get_text().strip()
                    author = f'{author}, {author2}'
                except:
                    author = s.select(f'body > div:nth-child({increment}) > div.contributor > a:nth-child(1)')[
                        0].get_text().strip()
            try:
                partial_link = result.get('href')
                link = 'https://www.penguinrandomhouse.com' + partial_link
                first_browser = start_chrome(link, headless=True)
                d = BeautifulSoup(first_browser.page_source, 'html.parser')
                try:
                    book_type = d.select(
                        f'#mobileList > div > div.bookRow.active > div.bk_row_wrap > div.dataDiv > div.frmtName > span.frmt-text')[0].get_text().strip()
                    if book_type != 'Paperback':
                        if book_type != 'Hardcover':
                            response.close()
                            increment = increment + int(1)
                            continue
                except:
                    book_type = 'BOOK TYPE UNKNOWN'
                try:
                    title = d.select(
                        f'#main_facade > div > div > div.main-content.col-xs-14.col-sm-16.col-md-16.col-lg-16 > div.product-header.clearfix > div.slot.product-title > div > h1')[0].get_text().strip()
                except:
                    title = 'TITLE UNAVAILABLE'
                try:
                    isbn = d.select(
                        f'#mobileList > div.activeBookRow > div.bookRow.active > div.bk_row_wrap > div.dataDiv > div.frmtInfo > span:nth-child(3)')[0].get_text().strip('ISBN ')
                except:
                    isbn = 'ISBN UNAVAILABLE'
                try:
                    category = d.find(
                        "h4", {"class": "category"}).get_text().strip().replace('Category: ', '')
                except:
                    category = 'CATEGORY UNAVAILABLE'
                try:
                    pages = d.find_all(
                        "span", {"class": "ws-nw"})
                    for page in pages:
                        if "Pages" in page.get_text().strip():
                            pages = page.get_text().strip().replace('| ', '')
                            pages = pages.replace(' Pages', '')
                            break
                        else:
                            pages = 'PAGES UNKOWN'
                except:
                    # NO IMAGE
                    pages = 'PAGES UNKNOWN'
                try:
                    dates = ['Jan ', 'Feb ', 'Mar ', 'Apr ', 'May ', 'Jun ',
                             'Jul ', 'Aug ', 'Sep ', 'Oct ', 'Nov ', 'Dec ']
                    release_date = d.find_all(
                        "span", {"class": "ws-nw"})
                    for page in release_date:
                        if any(x in page.get_text().strip() for x in dates):
                            release_date = page.get_text().strip()
                            break
                        else:
                            release_date = 'DATE UNKNOWN'
                except:
                    # NO DATE
                    release_date = 'DATE UNKNOWN'
                # try:
                #     price = d.select(
                #         f'#mobileList > div > div.bookRow.active > div.bk_row_wrap > div.dataDiv > div.frmtName > span.mobile-us-price')[0].get_text().strip()
                # except:
                #     price = 'PRICE UNAVAILABLE'
                try:
                    cover = d.select(
                        f'#mobileList > div > div.bookRow.active > div.bk_row_wrap > div.imageDiv > img')[0].get('src')
                except:
                    cover = 'COVER UNAVAILABLE'
                first_browser.quit()
            except:
                first_browser = 'NO FIRST BROWSER AVAILABLE'
            try:
                isbn_url = 'https://www.amazon.com/s?k=' + str(isbn)
                isbn_response = requests.get(isbn_url, headers=amazon_headers)
                isbn_page_text = isbn_response.text.encode(
                    'utf-8').decode('ascii', 'ignore')
                z = BeautifulSoup(isbn_page_text, features='lxml')
                try:
                    for a in z.find_all('a', href=True):
                        find_amazon = a.get('href')
                        if f'keywords={isbn}' in find_amazon:
                            amazon = find_amazon
                            amazon = 'https://www.amazon.com' + str(amazon)
                            break
                    if amazon == '-':
                        response.close()
                        increment = increment + int(1)
                        continue
                except:
                    amazon = 'NO AMAZON LINK'
                isbn_response.close()
            except:
                # NO ISBN URL
                isbn_url = 'NO ISBN URL'
            try:
                amazon_response = requests.get(amazon, headers=amazon_headers)
                page_text = amazon_response.text.encode(
                    'utf-8').decode('ascii', 'ignore')
                a = BeautifulSoup(page_text, features='lxml')
                for amaz in a.find_all('a', href=True):
                    prices = amaz.get('href')
                    if 'tmm_aud_swatch' in prices:
                        amazon_response.close()
                        aud_response = prices
                        aud_response = 'https://www.amazon.com' + \
                            str(aud_response)
                        a_response = requests.get(
                            aud_response, headers=amazon_headers)
                        a_page_text = a_response.text.encode(
                            'utf-8').decode('ascii', 'ignore')
                        a = BeautifulSoup(a_page_text, features='lxml')
                        a_response.close()
                    elif 'tmm_kin_swatch' in prices:
                        amazon_response.close()
                        kin_response = prices
                        kin_response = 'https://www.amazon.com' + \
                            str(kin_response)
                        k_response = requests.get(
                            kin_response, headers=amazon_headers)
                        k_page_text = k_response.text.encode(
                            'utf-8').decode('ascii', 'ignore')
                        a = BeautifulSoup(k_page_text, features='lxml')
                        k_response.close()
                try:
                    hrd = int(0)
                    pap = int(0)
                    for ama in a.find_all('a', href=True):
                        prices = ama.get('href')
                        if 'tmm_hrd_swatch' in prices and hrd == 0:
                            hardcover_response = prices
                            hardcover_response = 'https://www.amazon.com' + \
                                str(hardcover_response)
                            h_response = requests.get(
                                hardcover_response, headers=amazon_headers)
                            h_page_text = h_response.text.encode(
                                'utf-8').decode('ascii', 'ignore')
                            h = BeautifulSoup(h_page_text, features='lxml')
                            try:
                                for i in h.find_all('span', {'class': 'a-size-base a-color-price a-color-price'}):
                                    hardcover = i.get_text().strip()
                            except:
                                hardcover = 'HARDCOVER NOT FOUND'
                            hrd = hrd + int(1)
                            h_response.close()

                        if 'tmm_pap_swatch' in prices and pap == 0:
                            paperback_response = prices
                            paperback_response = 'https://www.amazon.com' + \
                                str(paperback_response)
                            p_response = requests.get(
                                paperback_response, headers=amazon_headers)
                            p_page_text = p_response.text.encode(
                                'utf-8').decode('ascii', 'ignore')
                            p = BeautifulSoup(p_page_text, features='lxml')
                            try:
                                for j in p.find_all('span', {'class': 'a-size-base a-color-price a-color-price'}):
                                    paperback = j.get_text().strip()
                            except:
                                paperback = 'PAPERBACK NOT FOUND'
                            pap = pap + int(1)
                            p_response.close()
                    if hardcover == '-' and paperback == '-':
                        try:
                            for i in a.find_all('span', {'class': 'a-text-bold'}):
                                if 'Paperback' in i.get_text().strip():
                                    for i in a.find_all('span', {'class': 'a-size-base a-color-price a-color-price'}):
                                        paperback = i.get_text().strip()
                                elif 'Hardcover' in i.get_text().strip():
                                    for i in a.find_all('span', {'class': 'a-size-base a-color-price a-color-price'}):
                                        hardcover = i.get_text().strip()
                        except:
                            hardcover = '-'
                            paperback = '-'
                except:
                    # NO AMAZON
                    prices = 'NO AMAZON LINK'
                try:
                    rating = a.select('#acrCustomerReviewText')[
                        0].get_text().strip().replace(' ratings', '').replace(' rating', '')
                except:
                    rating = '-'
                try:
                    stars = a.select(
                        '#reviewsMedley > div > div.a-fixed-left-grid-col.a-col-left > div.a-section.a-spacing-none.a-spacing-top-mini.cr-widget-ACR > div.a-fixed-left-grid.AverageCustomerReviews.a-spacing-small > div > div.a-fixed-left-grid-col.aok-align-center.a-col-right > div > span > span')[0].get_text().strip().replace(' out of 5', '')
                except:
                    stars = '-'
                amazon_response.close()
            except:
                amazon_response = 'NO AMAZON RESPONSE AVAILABLE'
            print()
            print(f'INCREMENT: {increment}')
            print(f'TITLE: {title}')
            print(f'AUTHOR: {author}')
            print(f'ISBN: {isbn}')
            print(f'CATEGORY: {category}')
            print(f'PAGES: {pages}')
            print(f'RELEASE DATE: {release_date}')
            print(f'PAPERBACK: {paperback}')
            print(f'HARDCOVER: {hardcover}')
            print(f'RATINGS: {rating}')
            print(f'STARS: {stars}')
            print(f'BOOK COVER: {cover}')
            print(f'AMAZON LINK: {amazon}')
            print()
            print(f'{title},{author},{isbn},{category},{pages},{release_date},{paperback},{hardcover},{rating},{stars},{cover},{amazon}')
            increment = increment + int(1)
            # f = open('penguin_books.csv', 'a', newline='')
            # book = (title, author, category, pages, release_date,
            #         paperback, hardcover, rating, stars, cover, amazon)
            # writer = csv.writer(f)
            # writer.writerow(book)
            # f.close()
        except:
            print()
            print(f'{increment}: ERROR.')
            increment = increment + int(1)
    response.close()
