from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import pandas as pd
import numpy as np
import requests 
import re 
import certifi
import urllib3
import time
import csv

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

url = "https://www.flipkart.com/search?q=graphics+card&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3DMax"
main_url = 'https://www.flipkart.com'


link_list = []
modal_price = []
modal_name = []
modal_rating = []
modal_img = []
modal_rating_count = []
modal_review_count = []
collection_time = []
primary_data = pd.read_csv("result.csv")


#collects link of all gpu in flipkart from all pages
def links_collector(url,main_url):
    old = 0;
    new = 10;
    p_count = 1;
    while(old!=new):
        old = new
        response = ''
        while response == '':
            try:
                response = requests.get(url+'&page='+str(p_count), headers=headers)
                break
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                time.sleep(5)
                print("Was a nice sleep, now let me continue...")
                continue
        data = bs(response.content,'html.parser')
        formatted = bs(data.prettify(),'html.parser')
        links = formatted.find_all('a',{"class": "wjcEIp"})
        for link in links:
            link_list.append(main_url+link.get('href'))
        new = len(link_list)  
        p_count = p_count+1


#collects product images from the above collected link
def data_collector(link_list):
    for img in tqdm(link_list):
        page = ''
        while page == '':
            # this block executes until the server blocks the user and then waits for 5 second to continue with the loop
            try:
                page = img
                next_page = requests.get(page, headers=headers)
                break
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                time.sleep(5)
                print("Was a nice sleep, now let me continue...")
                continue
        clean_page = bs(next_page.content,'html.parser')
        format_page = bs(clean_page.prettify(),'html.parser')
        images = format_page.find('img',{"class": "DByuf4 IZexXJ jLEJ7H"})
        price = format_page.find('div',{"class": "Nx9bqj CxhGGd"})
        rating = format_page.find('div',{"class": "ipqd2A"})
        name = format_page.find('span',{"class": "VU-ZEz"})
        r_count = format_page.find('span',{"class": "Wphh3N"})
        if(price == None or int(price.get_text().strip()[1:].replace(",","")) < 10000):
            modal_name.append("NULL")
            modal_price.append("NULL")
            modal_img.append("NULL")
            modal_rating.append("NULL")
            modal_rating_count.append("NULL")
            modal_review_count.append("NULL")
            collection_time.append('/'.join(time.ctime(time.time()).split()[1:]))
        else:
            if(rating == None):
                modal_rating.append("No rating")
                modal_rating_count.append("No rating ")
                modal_review_count.append("No rating ")
            else:
                modal_rating.append(rating.get_text().split())
                modal_rating_count.append(r_count.get_text().split()[0])
                modal_review_count.append(r_count.get_text().split()[3])
                
            modal_name.append(images.get('alt'))
            modal_price.append(int(price.get_text().strip()[1:].replace(",","")))
            modal_img.append(images.get('src'))
            collection_time.append('/'.join(time.ctime(time.time()).split()[1:]))



links_collector(url,main_url)
data_collector(link_list)


df = pd.DataFrame(data={"modal_name": modal_name, "modal_price": modal_price,"modal_rating": modal_rating, "modal_img": modal_img,"modal_rating_count": modal_rating_count, "modal_review_count": modal_review_count,"time":collection_time})
length = len(primary_data)
primary_data = pd.concat([primary_data,df],ignore_index=True)
primary_data.iloc[length:].to_csv('result.csv', mode='a', header=False,index=False)