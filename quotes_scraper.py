import requests
from bs4 import BeautifulSoup
from time import sleep
from csv import DictWriter, DictReader
from os import path


def get_next_page(soup, base_address):
    next_button = soup.find(class_="next")
    next_url = base_address + \
        next_button.find("a")["href"] if next_button else None
    return next_url


def scrape_quotes(url):
    current_url = url
    quotes_data = []
    print("Loading Data:", end=" ", flush=True)

    while current_url:
        response = requests.get(current_url)
        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all(class_="quote")

        for quote in quotes:
            quotes_data.append({
                "text": quote.find(class_="text").get_text(),
                "author": quote.find(class_="author").get_text(),
                "bio-link": url + quote.find("a")['href']
            })

        current_url = get_next_page(soup, url)
        print(".", end="", flush=True)
        sleep(1)

    print()
    return quotes_data


def get_author_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    born_date = soup.find(class_="author-born-date").text
    born_location = soup.find(class_="author-born-location").text
    details = f"The author was born on {born_date}, {born_location}."
    return details


def read_quotes(filename):
    with open(filename, "r", encoding="utf8") as file:
        csv_reader = DictReader(file)
        return list(csv_reader)


def write_quotes(quotes):
    with open("quotes.csv", "w", encoding="utf8") as file:
        headers = ["text", "author", "bio-link"]
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        for quote in quotes:
            csv_writer.writerow(quote)


def user_reload(url):
    while True:
        if not path.isfile("quotes.csv"):
            reload = 'y'
        else:
            reload = input("Would you like to reload the data (y/n)? ").lower()
        if reload == 'n' or reload == 'y':
            message = ''
            if reload == 'y':
                write_quotes(scrape_quotes(url))
                message = "Done.\n"
            print(message)
            return
