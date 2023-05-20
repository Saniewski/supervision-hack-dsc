# Supervision_Hack 2

## Introduction
An entry for Supervison Hack 2 competition by team Data Science Club PJATK.

Problem picked - #FakeJobHunter

## Team
**Data Science Club PJATK**:
- Jacek Jackowski
- Piotr Kojałowicz
- Stanisław Raczkiewicz
- Paweł Saniewski
- Igor Winek

## Prerequisites
Requires setup of a virtual enviroment using provided `requirements.txt` file.

## Project Structure and Pipeline

- `01_scrappers`:
  This directory contains all notebooks and scripts used for crawling and scrapping data from various websites. These include:
  - `fb_scrapper`: A script for scrapping data from Facebook groups.
  - `Oglaszamy24_scrapper`: A script for scrapping data from Oglaszamy24 website.
  - `olx_crawler` and `OLX_link_opener`: A script for scrapping data from OLX website.
  - `topogl_crawler`: A script for scrapping data from TopOgloszenia website.
  - `uber-scrapper-new.py`: A script for scrapping data from all of the above sources using corresponding scrappers.
- `02_preprocessing`:
  This directory contains all notebooks and scripts used for preprocessing and cleaning data. These include:
  - `02_01_fake_job_hunter_dataprep.ipynb`: A notebook for preprocessing data provided by Fake Job Hunter competition hosts.
  - `02_02_fb_text_extracting_filtering.ipynb`: A notebook for preprocessing data scrapped from Facebook groups.
  - `02_03_ngram_duplicates.ipynb`: A notebook for retrieving duplicate n-grams in each job listing.
  - `02_04_join_datasets_into_final_dataset.ipynb`: A notebook for joining all datasets into one final dataset.
- `03_models`:
  This directory contains all notebooks and scripts used for training and evaluating models as well as saved weights. These include:
  - `03_01_polbert_embeddings.ipynb`: A notebook for tokenizing and embedding text data using Polish BERT model.
  - `03_02_clustering.ipynb`: A notebook for clustering job listings using K-Means algorithm. The 2-Means clustering provides labels for unlabeled data. This allows for training a supervised model.
  - `03_03_supervised_model.ipynb`: A notebook for training a supervised learning model using Random Forest classifier.
  - `03_04_test_model.ipynb`: A notebook for testing the trained model with supplied test file.
  - `03_05_rf_model.py`: A script for generating a prediction for provided job offer description as a command line argument after `--input` flag using trained Random Forest classifier.
- `04_app`: This directory contains a streamlit app used for predicting whether a job listing is fake or not.
- `data`: This directory contains all data (input and output) used in the project.
- `docs`: This directory contains pieces of documentation and reports.
- `infra`: This directory contains infrastructure planned for an end-to-end pipeline.

## Results summary
A short summary of the prediction results, dataset size, etc.

### Scrapping
- Facebook groups scraped: 42
- Facebook posts scraped: ca. 480
- OLX offers scraped: ca. 1300
- Oglaszamy24 offers scraped: ca. 1580
- TopOgloszenia offers scraped: ca. 1140
- JobHunter dataset size (labeled): 42
- GPT-generated dataset size (labeled): 22

### Models scores:
- K-Means clustering:
  - Accuracy: 0.66
  - Precision: 0.56
  - Recall: 0.89
  - F1: 0.69
- Random Forest:
  - Accuracy: 0.94
  - F1: 0.95
