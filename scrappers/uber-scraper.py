import os
import subprocess
import json
from pymongo import MongoClient

# List of your scraper scripts names (replace with your actual script names)
scraper_scripts = ["fb_scrapper.py", "scraper2.py", "scraper3.py"]

# MongoDB connection setup
client = MongoClient("mongodb://<user>:<password>@localhost:27017/")
db = client["webscraper_data"]
collection = db["scraped_data"]

# Run each scraper
for script in scraper_scripts:
    output_file_name = script[:-3] + "_output.json"

    # Run the scraper script and save the output to the specified JSON file
    with open(output_file_name, "w") as output_file:
        subprocess.run(["python", script], stdout=output_file)

    # Load the JSON file contents and send it to the MongoDB database
    with open(output_file_name, "r") as output_file:
        contents = json.load(output_file)
        collection.insert_one(contents)

print("Scraping completed and data saved to MongoDB")
