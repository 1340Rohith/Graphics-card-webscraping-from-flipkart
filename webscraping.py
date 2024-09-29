from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import pandas as pd
import numpy as np
import requests 
import re 
import certifi
import urllib3
import time

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

url = "https://www.flipkart.com/gaming/gaming-graphic-cards/pr?sid=4rr%2Ctin%2C6zn&q=nvidia+rtx+graphics+card&otracker=categorytree&p%5B%5D=facets.brand%255B%255D%3DnVIDIA&p%5B%5D=facets.brand%255B%255D%3DASUS&p%5B%5D=facets.brand%255B%255D%3DGIGABYTE&p%5B%5D=facets.brand%255B%255D%3DZOTAC&p%5B%5D=facets.brand%255B%255D%3DMSI&p%5B%5D=facets.brand%255B%255D%3DGeforce&p%5B%5D=facets.brand%255B%255D%3Dgigabtye"
main_url = 'https://www.flipkart.com'

link_list = []
modal_price = []
modal_name = []
modal_rating = []
modal_img = []


#collects link of all gpu in flipkart from all pages
old = 0;
new = 10;
p_count = 1;
while(old!=new):
    old = new
    response = requests.get(url+'&page='+str(p_count), headers=headers)
    data = bs(response.content,'html.parser')
    formatted = bs(data.prettify(),'html.parser')
    links = formatted.find_all('a',{"class": "wjcEIp"})
    for link in links:
        link_list.append(main_url+link.get('href'))
    new = len(link_list)  
    p_count = p_count+1

#collects product images from the above collected link
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
    modal_price.append(price)
    modal_img.append(images.get('src'))