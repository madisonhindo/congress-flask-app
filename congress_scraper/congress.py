import time
from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

newfile = open('list_of_urls.txt', 'w')

rep_list = ['?q={%22congress%22:116}&pageSize=250','?q=%7B%22congress%22%3A%22116%22%7D&pageSize=250&page=2', '?q=%7B%22congress%22%3A%22116%22%7D&pageSize=250&page=3']

def get_links(url):
    driver = webdriver.Chrome('/Users/madisonhindo/Documents/python/final_project/congress_scraper/chromedriver')
    rep_url = driver.get('https://www.congress.gov/members' + url)
    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")
    reps = bs.find_all('li', {'class' : 'expanded'})
    for rep in reps:
        link = rep.find('a')
        if 'href' in link.attrs:
            newfile.write(link.attrs['href'] +  '\n')
for link in rep_list:
    get_links(link)

newfile.close()
