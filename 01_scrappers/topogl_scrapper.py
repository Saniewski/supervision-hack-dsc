import csv
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.robotparser import RobotFileParser
from html import unescape
import re
import json

def clean_text(text):
    cleaned_text = unescape(text)  # Usunięcie oznaczeń HTML
    cleaned_text = re.sub(r"<.*?>", "", cleaned_text)  # Usunięcie oznaczeń HTML
    cleaned_text = re.sub(r"&#[0-9]+;", "", cleaned_text)  # Usunięcie odniesień do znaków Unicode
    cleaned_text = re.sub(r",", " ", cleaned_text)  # Zamiana przecinków na spacje
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)  # Usunięcie białych znaków (spacje, nowe linie)
    cleaned_text = cleaned_text.strip()  # Usunięcie białych znaków z początku i końca tekstu
    return cleaned_text

PATH = "/opt/homebrew/bin/chromedriver"

work_hrefs = pd.read_csv('../data/topogl_work_hrefs.csv')

options = Options()
options.add_argument('--headless') 
driver = webdriver.Chrome(PATH, options=options)

robot_parser = RobotFileParser()
robot_parser.set_url('https://top-ogloszenia.net/robots.txt')
robot_parser.read()

if not robot_parser.can_fetch('*', driver.current_url):
    print("Strona jest niedostępna dla skryptu.")
    driver.quit()
    exit()

with open('../data/topogl_work_descriptions.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'descriptions'])  

descriptions = []

for href in work_hrefs.iloc[:, 0]:
    href_full = 'https://top-ogloszenia.net/' + href
    id = href.rsplit("-", 1)[-1]  # Wyciągnięcie id

    driver.get(href_full)

    work_desc = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.product-description'))
    ).get_attribute('innerHTML')
    work_desc = clean_text(work_desc)
    descriptions.append({'id': id, 'description': work_desc})

    with open('../data/topogl_work_descriptions.csv', 'a') as csv_f:
        writer = csv.writer(csv_f)
        writer.writerow([id, work_desc])
    with open('../data/topogl_work_descriptions.json', 'w', encoding='utf-8') as json_f:
        json.dump(descriptions, json_f, ensure_ascii=False)

driver.quit()
