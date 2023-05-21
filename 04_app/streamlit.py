import streamlit as st
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import subprocess

def clean_text(text):
    cleaned_text = re.sub(r"<.*?>", "", text)
    cleaned_text = re.sub(r"&#[0-9]+;", "", cleaned_text)
    cleaned_text = re.sub(r",", " ", cleaned_text)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)
    cleaned_text = cleaned_text.strip()
    return cleaned_text

def scrape_text(url):
    options = Options()
    options.add_argument("--headless")
    service = Service("path/to/chromedriver")  # Replace with your chromedriver path
    driver = webdriver.Chrome(service=service, options=options)

    try:
        if 'top-ogloszenia.net' in url:
            driver.get(url)
            work_desc = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.product-description'))
            ).get_attribute('innerHTML')
            print(work_desc)
            return clean_text(work_desc)
        if 'oglaszamy24.pl' in url:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            description_element = soup.find("div", id="adv_desc")
            work_desc = description_element.text.strip()
            print(work_desc)
            return clean_text(work_desc)
        if 'olx.pl' in url:
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            html = soup.prettify()
            elements = soup.select('.css-19srbbu')
            work_desc = []
            for element in elements:
                work_desc.append(element.get_text())
            work_desc = work_desc[0]
            print(work_desc)
            return clean_text(work_desc)
    except:
        return False
    finally:
        driver.quit()

def fakehunter_predict(text):
    prediction = subprocess.run(["python", "../03_models/03_05_rf_model.py", "--input", text], capture_output=True)
    prediction_str = prediction.stdout.decode("utf-8").strip()
    return float(prediction_str[1])

def assign_conditions(prediction):
    conditions = {
        "fake": {"text": "OSZUSTWO", "color": "red", "func": st.error},
        # "maybe_fake": {"text": "Jest ryzyko", "color": "yellow", "func": st.warning},
        "non_fake": {"text": "Ogłoszenie wiarygodne", "color": "green", "func": st.success}
    }

    if prediction == 0:
        return conditions["fake"]
    else:
        return conditions["non_fake"]

st.title("Whistleblower on Web-scams - Sprawdzanie ogłoszeń o pracę")

tab = st.sidebar.selectbox("Wybierz zakładkę", ("Wstaw ogłoszenie", "Podaj link"))

if tab == "Wstaw ogłoszenie":
    text = st.text_area("Wpisz treść ogłoszenia o pracę", height=200)

    if st.button("Sprawdź ogłoszenie"):
        if text:
            prediction = fakehunter_predict(text)
            conditions = assign_conditions(prediction)
            if conditions["text"]:
                conditions["func"](conditions["text"])

elif tab == "Podaj link":
    url = st.text_input("Wprowadź link do ogłoszenia o pracę")

    if st.button("Sprawdź link"):
        if url:
            text = scrape_text(url)
            if text:
                probability = fakehunter_predict(text)
                st.markdown(text)
                st.markdown(f"**Prawdopodobieństwo oszustwa**: {probability:.2%}")
                conditions = assign_conditions(probability)
                if conditions["text"]:
                    conditions["func"](conditions["text"])
                st.text(f"{probability*100:.2f}%")
                st.markdown(
                    f'<progress value="{probability}" max="1" style="width: 100%; background-color: {conditions["color"]};"></progress>',
                    unsafe_allow_html=True
                )
            else:
                st.warning("Nie można zeskrapować tekstu ogłoszenia. Sprawdź wprowadzony link.")
