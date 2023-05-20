import os
import subprocess
import json
from pymongo import MongoClient

# List of your scraper scripts names (replace with your actual script names)
list_scripts = ["scraper1.py", "scraper2.py", "scraper3.py"]
list_files = [
                "/home/piotr/Activate/supervision-hack-dsc/data/fb.json",
                "/home/piotr/Activate/supervision-hack-dsc/data/olx_remote_work.json",
                "/home/piotr/Activate/supervision-hack-dsc/data/oglaszamy24.json"
              ]

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client["webscraper_data"]
collection = db["scraped_data"]


def run_subscrapper(scraper_scripts):
    for script in scraper_scripts:
        output_file_name = script[:-3] + "_output.json"

        # Run the scraper script and save the output to the specified JSON file
        with open(output_file_name, "w") as output_file:
            subprocess.run(["python", script], stdout=output_file)


def add_date_to_db(files):
    for file in files:
        # Load the JSON file contents and send it to the MongoDB database
        with open(file, 'r') as file_j:
            data = json.load(file_j)
            if isinstance(data, list):
                collection.insert_many(data)
            else:
                collection.insert_one(data)


if __name__ == "__main__":

    #run_subscrapper(list_scripts)
    add_date_to_db(list_files)
