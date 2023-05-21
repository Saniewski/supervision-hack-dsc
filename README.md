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

## Project Structure

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

## Pipeline

Our approach resembles a custom, semi-supervised learning pipeline. The pipeline consists of three main stages:

### **1. Scrapping data from Facebook groups, OLX, Oglaszamy24 and TopOgloszenia.**
For this, we used a combination of Selenium and BeautifulSoup libraries. All scrappers and web crawlers are present in the `01_scrappers` directory. All output data is dumped into the `data` directory.

### **2. Preprocessing, datat cleaning, and preparation of the final dataset.**
For this, we used a combination of Pandas, NLTK, and Spacy libraries. All preprocessing notebooks are present in the `02_preprocessing` directory. Again, the outputs of this stage are dumped into the `data` directory.

#### **2.1. Preprocessing of the data provided by the competition hosts.**
#### **2.2. Preprocessing of the data scrapped from Facebook groups.**
#### **2.3. Retrieving duplicate n-grams in each job listing.**
#### **2.4. Joining all datasets into one final dataset.**
At this stage, our final dataset looks like this:
| id | text | label |
| --- | --- | --- |
| *A unique identifier in form of a string used for referencing a row in the database and to reject duplicate data in the pipeline* | *Job listing description without interpunction, in lower case* | *NaN if the data row is scrapped, otherwise 1 if the job listing is trustworthy and 0 if it's a fake* |

### **3. Training and evaluating models.**
In this step, we used a combination of transformers, scikit-learn, and PyTorch libraries. All notebooks and scripts used for training and evaluating models are present in the `03_models` directory. The data inputs are retrieved from the `data` directory and the outputs are stored in the `data` directory.

#### **3.1. Tokenizing and embedding text data using Polish BERT model.**
This step utilizes the Polish BERT model (`dkleczek/bert-base-polish-uncased-v1`) to tokenize and embed text data. The output of this step is a dataset with embedded text data, and the output data looks as follows:
| id | text | label | embeddings |
| --- | --- | --- | --- |
| same as above | same as above | same as above | *A list of 768-dimensional embeddings for each word in the job listing description* |

#### **3.2. Clustering job listings using K-Means algorithm.**
This step runs the K-Means (2-Means binary classification) clustering algorithm on the embedded text data. In the process, a cluster ID is received and the label of the cluster is determined by the number of positives (trustworthy job listings) assigned to each cluster. Then, the label of each row is filled in based on the cluster ID the data sample was assigned to. The output of this step is a dataset with labels for each job listing, and the output data looks as follows:
| id | text | label | embeddings |
| --- | --- | --- | --- |
| same as above | same as above | *1 if the job listing is assigned to the cluster with the most trustworthy listings, otherwise 0* | same as above |

#### **3.3. Training a supervised learning model using Random Forest classifier.**
This step trains a Random Forest classifier on the training subset of the text data labeled by K-Means clustering. The job listing description is fitted and transformed using the TF-IDF algorithm, and the results of this and the provided labels are used to train the model. The output of this step is a trained model saved in the `03_models` directory as well as a fitted TF-IDF.

#### **3.4. Testing the trained model with a subset of prepared data.**
This step tests the trained Random Forest classifier on the test subset of the text data labeled by K-Means clustering. The output of this step is a classification report and a confusion matrix printed in the notebook. The script for retrieving predictions for the test subset is also provided in the `03_models` directory.

### **4. Application.**
The application is a simple Streamlit app that allows the user to input a job listing description or an URL to such listing and get a prediction whether the job listing is trustworthy or not. The app uses the trained Random Forest classifier to make the prediction and inform the user whether the job listing is trustworthy or suspicious.

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


## Further development
- Collect more data from other sources and integrate those sources in the application.
- Create microservices for each stage of the pipeline to automate the process in an end-to-end solution.
- Add a better persistence layer for the data.
  - Use MongoDB in pair with Qdrant for storing and querying the data and vectors of embeddings. (**In progress**)
- Add reporting and logging to the end user application.
- Create a browser extension for the end user to report suspicious internet activity in real time.
