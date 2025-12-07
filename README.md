# Elections Scraper

## Project Overview
The Elections Scraper is a Python-based tool designed to scrape election results from the official Czech election website https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ. The script extracts data for a specific electoral district and saves the results into a CSV file. The output includes detailed information about voters, envelopes, valid votes, and votes for each political party.

## Requirements
- Python 3.9 or higher
- Virtual environment (recommended)

## Installation
Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
The script is executed from the command line and requires two arguments:
1. **URL**: The URL of the electoral district to scrape.
2. **Output file**: The name of the CSV file where the results will be saved.

### Example
To scrape election results for the Benešov district and save the output to `vysledky_benesov.csv`, run the following command:
```bash
python main.py 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101' 'vysledky_benesov.csv'
```

### Output
Command line:
```bash
Please wait... Scraping data from https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101.
Results have been saved to benesov.csv.
```
The output CSV file will contain the following columns:
- `code`: Municipality code
- `location`: Municipality name
- `registered`: Number of registered voters
- `envelopes`: Number of issued envelopes
- `valid`: Number of valid votes
- One column for each political party, containing the number of votes received

### Sample Output of CSV File
code, location, registered, envelopes, valid, Občanská demokratická strana, Řád národa...  
529303,Benešov,13 104,8 485,8 437,1 052,10,2,624,3,802,597,109,35,112,6,11,948,3,6,414,2 577,3,21,314,5,58,17,16,682,10  
532568,Bernartice,191,148,148,4,0,0,17,0,6,7,1,4,0,0,0,7,0,0,3,39,0,0,37,0,3,0,0,20,0  
530743,Bílkovice,170,121,118,7,0,0,15,0,8,18,0,2,0,0,0,3,0,0,2,47,1,0,6,0,0,0,0,9,0  
...  

## Notes
- Ensure the URL provided is valid and points to an electoral district page.
- The output file must have a `.csv` extension.

## License
This project is licensed under the MIT License.
