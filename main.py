import time
from datetime import datetime
import requests
import selectorlib
import send_email
import sqlite3

URL = 'https://programmer100.pythonanywhere.com/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
date_format = "%y-%m-%d-%H-%M-%S"
connection = sqlite3.connect("./files/data.db")


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
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?)", (date, extracted))
    connection.commit()


def read(date, extracted):
    temp = extracted.split(",")
    temp = [item.strip() for item in temp]
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE date=? AND temperature=?", (date, temp[0]))
    if cursor is not None:
        temp = cursor.fetchall()
    else:
        return False
    return temp

if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    if extracted is not None:
        date = datetime.now()
        formatted_date = date.strftime(date_format)
        row = read(formatted_date, extracted)
        store(formatted_date, extracted)
        # send_email(message="Hey, this is the average temperature for today")
    time.sleep(2)