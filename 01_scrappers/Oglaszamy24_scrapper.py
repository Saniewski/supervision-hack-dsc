#!/usr/bin/env python
# coding: utf-8

# In[9]:


### Libraries
from selenium import webdriver
from lxml import html
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import pandas as pd

### URL adress
url = 'http://www.oglaszamy24.pl/ogloszenia/praca/oferty-pracy/?std=1&results='

### Links list
links_list = []
links_list_final = []

### Loop through the page number
for i in tqdm(range(81)):
    
    ### Download html code from site
    response = requests.get(url+str(i+1))
    soup = BeautifulSoup(response.content, 'html.parser')

    ### Founding evry single href with calass 'o_title'
    links = soup.find_all('a', class_='o_title')
    links_list = links_list + links

### Creating final clear list of links
for i in tqdm(links_list):
    links_list_final.append(i['href'])

### List to columns df     
titles = []
descriptions = []

### Jobs Scraper
for link in tqdm(links_list_final):

    ### Downloading web source
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")

    ### Downloading title
    title_element = soup.find("h1", class_="std_h1")
    title = title_element.text.strip() if title_element else ""

    ### Downloading descriptions
    description_element = soup.find("div", id="adv_desc")
    description = description_element.text.strip() if description_element else ""

    ### Adding title and description to lists
    titles.append(title)
    descriptions.append(description)


### Creating dataframe
df = pd.DataFrame({"Title": titles, "Description": descriptions})

### Data Export
df.to_csv('../data/oglaszamy24.csv', index=False)
with open('../data/oglaszamy24.json', 'w', encoding='utf-8') as f:
  df.to_json(f, force_ascii=False, orient='records')


# In[3]:




