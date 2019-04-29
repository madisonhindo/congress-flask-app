import time
import requests
from selenium import webdriver
from urllib.request import urlopen
from functools import reduce
from bs4 import BeautifulSoup
import csv


base_url = 'https://www.congress.gov/members'

hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

session = requests.Session()
req = session.get(base_url, headers=hdr)
bs = BeautifulSoup(req.text, "html.parser")

rep_list = ['?q={%22congress%22:116}&pageSize=250','?q=%7B%22congress%22%3A%22116%22%7D&pageSize=250&page=2', '?q=%7B%22congress%22%3A%22116%22%7D&pageSize=250&page=3']
rep_links = []

def get_links(url):
    global rep_links
    for rep in rep_list:
        url = base_url + rep
        session = requests.Session()
        req = session.get(url, headers=hdr)
        bs = BeautifulSoup(req.text, "html.parser")
        reps = bs.find_all('li', {'class' : 'expanded'})
        for rep in reps:
                link = rep.find('a')            
                if 'href' in link.attrs:
                        rep_links.append(link.attrs['href'])

get_links(rep_list)

newfile = open('rep_info_full.csv', 'w') 
c = csv.writer(newfile)
c.writerow(['name', ' state', ' district', ' office time', ' website', ' contact', ' party'])


def scrape_members(links):
        for link in links:
                session = requests.Session()
                req = session.get(link, headers=hdr)
                bs = BeautifulSoup(req.text, "html.parser")
                contact_list = []
                table_two = bs.find('table').find_next('table').find('tr')
                contact = table_two.find_next('tr').find('td').get_text()
                contact_split = contact.split('(')
                contact_list.append(contact_split)

                global representative_info
        print(contact_list)
                        
scrape_members(rep_links)
newfile.close()