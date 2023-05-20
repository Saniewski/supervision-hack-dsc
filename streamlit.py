import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

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
            return clean_text(work_desc)
    except:
        return False
    finally:
        driver.quit()

def fakehunter_predict(text):
    # Your FakeHunter model prediction logic here
    import random
    probability = random.uniform(0, 1)
    return probability

def assign_conditions(probability):
    conditions = {
        "fake": {"text": "OSZUST", "color": "red", "func": st.error},
        "maybe_fake": {"text": "Jest ryzyko", "color": "yellow", "func": st.warning},
        "non_fake": {"text": "Nie ma oszustwa", "color": "green", "func": st.success}
    }

    if probability > 0.85:
        return conditions["fake"]
    elif 0.6 <= probability <= 0.85:
        return conditions["maybe_fake"]
    else:
        return conditions["non_fake"]

st.title("FakeHunter - Sprawdzanie ogłoszeń o pracę")

tab = st.sidebar.selectbox("Wybierz zakładkę", ("Wstaw ogłoszenie", "Podaj link"))

if tab == "Wstaw ogłoszenie":
    text = st.text_area("Wpisz treść ogłoszenia o pracę", height=200)

    if st.button("Sprawdź ogłoszenie"):
        if text:
            probability = fakehunter_predict(text)
            st.markdown(f"**Prawdopodobieństwo oszustwa**: {probability:.2%}")
            conditions = assign_conditions(probability)
            if conditions["text"]:
                conditions["func"](conditions["text"])
            st.text(f"{probability*100:.2f}%")
            st.markdown(
                f'<progress value="{probability}" max="1" style="width: 100%; background-color: {conditions["color"]};"></progress>',
                unsafe_allow_html=True
            )

elif tab == "Podaj link":
    url = st.text_input("Wprowadź link do ogłoszenia o pracę")

    if st.button("Sprawdź link"):
        if url:
            text = scrape_text(url)
            if text:
                probability = fakehunter_predict(text)
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
