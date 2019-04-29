import time
import requests
from urllib.request import urlopen
from functools import reduce
from bs4 import BeautifulSoup
import csv


base_url = 'https://www.opensecrets.org/states/summary.php?state='
base_industry_url = 'https://www.opensecrets.org/states/indus.php?cycle=2018&state='

hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

newfile = open('state_financial_info.csv', 'w') 
c = csv.writer(newfile)
c.writerow(['state', ' total_itemized_contributions', ' total_contributions_rank', ' top_industry', ' second_industry', ' third_industry', ' fourth_industry', ' fifth industry'])

state_abbreviations = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY',  'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
urls = []
def get_state_links():
       global urls
       for state in state_abbreviations:
              state_url = base_url + state
              urls.append(state_url)

get_state_links()

state_name = []

def get_state_name(url):
       global state_name
       for url in urls:
              session = requests.Session()
              req = session.get(url, headers=hdr)
              bs = BeautifulSoup(req.text, "html.parser")
              state = bs.find('h1').get_text()
              state_name.append(state)

get_state_name(urls)

total_itemized_contributions_list = []
itemized_contributions_rank_list = []

def state_contributions(url):
       global total_itemized_contributions_list
       global itemized_contributions_rank_list
       for url in urls:
              session = requests.Session()
              req = session.get(url, headers=hdr)
              bs = BeautifulSoup(req.text, "html.parser")
              base_table = bs.find('table', {'class' : 'datadisplay'})
              total_itemized_contributions = base_table.find('tr').find_next('tr').find('td').find_next('td').get_text()
              total_itemized_contributions_list.append(total_itemized_contributions)
              itemized_contributions_rank = base_table.find('tr').find_next('tr').find('td').find_next('td').find_next('td').get_text()
              itemized_contributions_rank_list.append(itemized_contributions_rank)

       #print(total_itemized_contributions_list)
       #print(itemized_contributions_rank_list)

state_contributions(urls)

industry_urls = []

def get_state_industry_links():
       global industry_urls
       for state in state_abbreviations:
              state_industry_url = base_industry_url + state
              industry_urls.append(state_industry_url)
       #print(industry_urls)
get_state_industry_links() 


top_industry_list = []
second_industry_list = []
third_industry_list = []
fourth_industry_list = []
fifth_industry_list = []

def get_industry_information(url):
       global top_industry_list
       global second_industry_list
       global third_industry_list
       global fourth_industry_list
       global fifth_industry_list
       for url in industry_urls:
              session = requests.Session()
              req = session.get(url, headers=hdr)
              bs = BeautifulSoup(req.text, "html.parser")
              base_industry_table = bs.find('table', {'class' : 'datadisplay'})
              top_industry = base_industry_table.find('td').get_text()
              top_industry_list.append(top_industry)
              second_industry = base_industry_table.find('tr').find_next('tr').find('td').get_text()
              second_industry_list.append(second_industry)
              third_industry = base_industry_table.find('tr').find_next('tr').find_next('tr').find('td').get_text()
              third_industry_list.append(third_industry)
              fourth_industry = base_industry_table.find('tr').find_next('tr').find_next('tr').find_next('tr').find('td').get_text()
              fourth_industry_list.append(fourth_industry)
              fifth_industry = base_industry_table.find('tr').find_next('tr').find_next('tr').find_next('tr').find_next('tr').find('td').get_text()
              fifth_industry_list.append(fifth_industry)
              
get_industry_information(industry_urls)

for row in zip(state_name, total_itemized_contributions_list, itemized_contributions_rank_list, top_industry_list, second_industry_list, third_industry_list, fourth_industry_list, fifth_industry_list):
       c.writerow(row)
