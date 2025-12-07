import argparse
import csv
import requests
from bs4 import BeautifulSoup

def validate_url(url: str) -> bool:
    """Validate if the provided URL is correct."""
    protocol = ("http://", "https://")
    return url.startswith(protocol)

def validate_output_file(filename: str) -> bool:
    """Validate if the output file has a .csv extension."""
    return filename.endswith('.csv')

def parse_arguments():
    """Parse and validate command-line arguments."""
    parser = argparse.ArgumentParser(description="Elections Scraper")
    parser.add_argument("url", type=str, help="URL of the electoral district")
    parser.add_argument("output", type=str, help="Name of the output CSV file")
    args = parser.parse_args()

    # Validate URL
    if not validate_url(args.url):
        print("Error: The provided URL is not valid.")
        exit(1)

    # Validate output file extension
    if not validate_output_file(args.output):
        print("Error: The output file must have a .csv extension.")
        exit(1)

    return args

def scrape_main_table(url: str) -> list:
    """Scrapes the main table of electoral districts."""
    response = requests.get(url)
    if response.status_code != 200:
        print("Error: Failed to fetch data from the URL. HTTP status code:", response.status_code)
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
                    'link': f"https://www.volby.cz/pls/ps2017nss/"
                        f"{link['href']}"
                })
    return data

def scrape_voting_results(link: str) -> dict:
    """Scrapes voting results for a specific municipality."""
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = {
        'registered': soup.find(headers='sa2').text, # voters on the list 
        'envelopes': soup.find(headers='sa3').text,  # issued envelopes  
        'valid': soup.find(headers='sa6').text       # valid votes
    }

    # Scrape political parties and their vote counts from all tables
    # except the first table which contains summary data
    party_tables = soup.find_all('table')[1:]  
    parties = {}

    for table in party_tables:
        rows = table.find_all('tr')[2:]  # Skip header rows
        for row in rows:
            cells = row.find_all('td')
            # Valid party row
            if len(cells) == 5 and (cells[0].text.strip() != "-"):  
                party_name = cells[1].text.strip()
                votes = cells[2].text.strip()
                parties[party_name] = votes

    results['parties'] = parties

    return results

def save_to_csv(data: list, filename: str):
    """Saves the scraped data to a CSV file."""
    # Collect all party names from the data in order of appearance
    all_parties = []
    for row in data:
        if 'parties' in row:
            for party in row['parties'].keys():
                if party not in all_parties:
                    all_parties.append(party)

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # CSV header
        header = [
            "code", 
            "location", 
            "registered", 
            "envelopes", 
            "valid"
        ] + all_parties
        writer.writerow(header)
        # CSV rows
        for row in data:
            # Get votes for each party or 0
            party_votes = [
                row['parties'].get(party, 0) 
                for party in all_parties
            ]
            writer.writerow([
                row['code'],
                row['name'],
                row['registered'],
                row['envelopes'],
                row['valid'],
                *party_votes
            ])

def main(url):
    # Scrape the main table
    main_data = scrape_main_table(url)
    results = {}
    all_results = []

    # Scrape voting results for each municipality
    for item in main_data:
        results = scrape_voting_results(item['link'])
        results['code'] = item['code']
        results['name'] = item['name']
            
        # Ensure 'code' and 'name' are the first keys in the result dictionary
        ordered_results = {
            'code': results['code'],
            'name': results['name'],
            **{k: v for k, v in results.items() if k not in ['code', 'name']}
        }
        all_results.append(ordered_results)

    return all_results


if __name__ == "__main__":

    args = parse_arguments()
    # Scrape the tables and save to CSV
    print(f"Please wait... Scraping data from {args.url}.")
    save_to_csv(main(args.url), args.output)
    print(f"Results have been saved to {args.output}.")
