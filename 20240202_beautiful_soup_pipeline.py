"""
Description: Data pipeline parsing with BeautifulSoup.

Date: Fri. 2/2/24 @ 3:01 PM EST
"""

# Importing the required libraries.
import requests
from bs4 import BeautifulSoup
import json

# Doing a GET request and saving the response.
def fetch_data(url):
    response = requests.get(url)
    return response.text

# Parsing the html using BeautifulSoup. Find all the <p> tags
# and if the id attibutes exist, then save the id attribute and
# the corresponding value in a dictionary.
def parse_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = {}
    for tag in soup.find_all('p'):
        key = tag.get('id')
        value = tag.text
        if key:
            data[key] = value
    return data

# Transform the data.
def transform_data(data):
    """TBD: When you need to transform the data, modify this section."""
    return data

# Data dump to store the data as json.
def write_data(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f)

# The data pipeline to run the sequence of steps in the data pipeline.
# Run fetch_data(), then parse_data(), then transform_data(), and lastly
# write_data().
def main(url, output_file_path):
    html = fetch_data(url)
    data = parse_data(html)
    data = transform_data(data)
    write_data(data, output_file_path)

# Run the pipeline
main('https://example.com', 'output.json')
