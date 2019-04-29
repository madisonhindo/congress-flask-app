import time
import requests
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

get_links(rep_links)

newfile = open('rep_info_test.csv', 'w') 
c = csv.writer(newfile)
c.writerow(['name', ' state', ' district', ' office time', ' website', ' contact', ' party'])

name_list = []
list_of_lists = []
state_list = []
district_list = []
office_time_list = []
website_list = []
contact_list = []
party_list = []
links = []

def get_names(links):
        global list_of_lists
        global name_list
        for link in links:
                session = requests.Session()
                req = session.get(link, headers=hdr)
                bs = BeautifulSoup(req.text, "html.parser")
                base = bs.find('div', {'class': 'breadcrumbs'}).get_text().strip()
                name = base.split('>', 2)
                name.pop(0)
                name.remove(' Members ')
                list_of_lists.append(name)
        name_list = reduce(list.__add__, list_of_lists)

def get_states(links):
     for link in links:
        session = requests.Session()
        req = session.get(link, headers=hdr)
        bs = BeautifulSoup(req.text, "html.parser")
        global state_list 
        base_info = bs.find('tbody').find('tr').find('td')
        state = base_info.get_text()
        state_list.append(state)

def get_districts(links):
     for link in links:
        session = requests.Session()
        req = session.get(link, headers=hdr)
        bs = BeautifulSoup(req.text, "html.parser")
        global district_list
        base_info = bs.find('tbody').find('tr').find('td')
        district = base_info.find_next('td').get_text()
        district_list.append(district.strip())

def get_office_length(links):
     for link in links:
        session = requests.Session()
        req = session.get(link, headers=hdr)
        bs = BeautifulSoup(req.text, "html.parser")
        global office_time_list
        base_info = bs.find('tbody').find('tr').find('td')
        office_time = base_info.find_next('td').find_next('td').get_text()
        office_time_list.append(office_time.strip())

def get_website_link(links):
     for link in links:
        session = requests.Session()
        req = session.get(link, headers=hdr)
        bs = BeautifulSoup(req.text, "html.parser")
        global website_list
        table_two = bs.find('table').find_next('table').find('tr')
        website = table_two.find('td').find('a')
        website_list.append(website.string.strip())

def get_contact_info(links):
     for link in links:
        session = requests.Session()
        req = session.get(link, headers=hdr)
        bs = BeautifulSoup(req.text, "html.parser")
        global contact_list
        table_two = bs.find('table').find_next('table').find('tr')
        contact = table_two.find_next('tr').find('td').get_text()
        contact_list.append(contact.strip())

def get_party_info(links):
     for link in links:
        session = requests.Session()
        req = session.get(link, headers=hdr)
        bs = BeautifulSoup(req.text, "html.parser")     
        global party_list
        table_two = bs.find('table').find_next('table').find('tr')
        party = table_two.find_next('tr').find_next('tr').find('td').get_text()
        party_list.append(party.strip())


for row in zip(name_list, state_list, district_list, office_time_list, website_list, contact_list, party_list):
        c.writerow(row)
        
                        
get_names(rep_links)
get_states(rep_links)
get_districts(rep_links)
get_office_length(rep_links)
get_website_link(rep_links)
get_contact_info(rep_links)
get_party_info(rep_links)
newfile.close()