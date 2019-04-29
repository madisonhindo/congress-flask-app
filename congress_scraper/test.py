import time
from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import time
from functools import reduce
driver = webdriver.Chrome('/Users/madisonhindo/Documents/python/final_project/congress_scraper/chromedriver')
rep_url = driver.get('https://www.congress.gov/members?q=%7B%22congress%22%3A116%7D')

html = driver.page_source
bs = BeautifulSoup(html, "html.parser")

reps = bs.find_all('li', {'class' : 'expanded'})

links = []
representative_info = []


for rep in reps:
    links.append(rep.find('a').attrs['href'] )

newfile = open('rep_info.csv', 'w') 
c = csv.writer(newfile)
c.writerow(['name', ' state', ' district', ' office time', ' website', ' contact', 'party'])

list_of_lists = []
name_list = []

def get_names(links):
        global list_of_lists
        global name_list
        for link in links:
                driver.get(link)
                html = driver.page_source
                bs = BeautifulSoup(html, 'html.parser')
                base = bs.find('div', {'class': 'breadcrumbs'}).get_text().strip()
                name = base.split('>', 2)
                name.pop(0)
                name.remove(' Members ')
                list_of_lists.append(name)
        name_list = reduce(list.__add__, list_of_lists)

def get_stuff(links):
        for link in links:
                driver.get(link)
                html = driver.page_source
                bs = BeautifulSoup(html, 'html.parser')
                name_list = []
                list_of_lists = []
                state_list = []
                district_list = []
                office_time_list = []
                website_list = []
                contact_list = []
                party_list = []
                base = bs.find('div', {'class': 'breadcrumbs'}).get_text().strip()
                name = base.split('>', 2)
                name.pop(0)
                name.remove(' Members ')
                list_of_lists.append(name)
                name_list = reduce(list.__add__, list_of_lists)
                base_info = bs.find('tbody').find('tr').find('td')
                state = base_info.get_text()
                state_list.append(state)
                district = base_info.find_next('td').get_text()
                district_list.append(district.strip())
                office_time = base_info.find_next('td').find_next('td').get_text()
                office_time_list.append(office_time.strip())
                table_two = bs.find('table').find_next('table').find('tr')
                website = table_two.find('td').find('a')
                website_list.append(website.string.strip())
                contact = table_two.find_next('tr').find('td').get_text()
                contact_list.append(contact.strip())
                party = table_two.find_next('tr').find_next('tr').find('td').get_text()
                party_list.append(party.strip())
                global representative_info
                name_list = reduce(list.__add__, list_of_lists)
                for row in zip(name_list, state_list, district_list, office_time_list, website_list, contact_list, party_list):
                        c.writerow(row)
        
get_stuff(links)
newfile.close()