import argparse
import csv
import requests
from bs4 import BeautifulSoup

def scrape_main_table(url: str) -> list:
    """Scrapes the main table of electoral districts."""
    response = requests.get(url)
    if response.status_code != 200:
        print("Error: Failed to fetch data from the URL.")
        exit(1)

    soup = BeautifulSoup(response.text, 'html.parser')
    table_rows = soup.find_all('tr')
    data = []

    for row in table_rows:
        cells = row.find_all('td')
        if cells:
            link = cells[0].find('a')
            if link:
                data.append({
                    'code': cells[0].text.strip(),
                    'name': cells[1].text.strip(),
                    'link': link['href']
                })
    return data

def scrape_voting_results(link: str) -> dict:
    pass

def save_to_csv(data: list, filename: str):
    pass


if __name__ == "__main__":

    args = [
        "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103", 
        "vysledky_prostejov.csv"
    ]

    # Scrape the main table
    main_data = scrape_main_table(args[0])
    print(main_data)    
    all_results = []
