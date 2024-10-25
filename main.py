import time
from datetime import datetime
import requests
import selectorlib
import send_email

URL = 'https://programmer100.pythonanywhere.com/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
date_format = "%y-%m-%d-%H-%M-%S"

def scrape(url):
    """ Scrape the page source from the URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["temperature"]
    return value


def store(date, extracted):
    with open("data.csv", "a") as file:
        file.write(f"{date},{extracted}" + "\n")


def read(extracted):
    with open("data.csv", "r") as file:
        return file.read()

if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    content = read(extracted)
    if extracted is not None:
        if extracted not in "data.csv":
            date = datetime.now()
            formatted_date = date.strftime(date_format)
            store(formatted_date, extracted)
            send_email.send_email(message="Hey, this is the average temp for today.")
    time.sleep(2)