# Loading required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

# We will follow the Extract, Transform & Load(ETL) process for this web scraping

# Setup logging
logging.basicConfig(level=logging.INFO)


def extract(url):
    """This function sets custom user-agent to mimic browser request, then uses GET request to the URL
    & if the response is a success(200), returns parsed HTML using BeautifulSoap. Also logs error.

    Args:
        url: Website URL we want to parse
        
    Returns:
        HTML: return parsed HTML
    """
    headers = {"User-Agent": "Enter-user-agent-here"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        parse = BeautifulSoup(response.content, "html.parser")
        return parse
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error:{e}")
        return None


def transform(parse):
    """The function initializes an empty list then parses the table for all rows & columns.
    Then appends the extracted data into the empty list of dictionary.

    Args:
        parse (HTML): Takes in parsed HTML from previous function as input

    Returns:
        list: Returns yahoolist that has appended all extracted columsn from ETF table
    """
    yahoolist = []
    if parse:
        table = parse.find("table", class_="markets-table")
        rows = table.find_all("tr")
        for item in rows:
            cols = item.find_all("td", class_="yf-paf8n5")
            if len(cols) <= 8:
                continue

            # Extract data from columns
            symbol = cols[0].text.strip()
            name = cols[1].text.strip()
            price = cols[2].text.strip()
            change = cols[3].text.strip()
            change_perc = cols[4].text.strip()
            volume = cols[5].text.strip()
            fiftydayavg = cols[6].text.strip()
            twohundreddayavg = cols[7].text.strip()

            # Append extracted data to the list
            yahoo = {
                "Symbol": symbol,
                "Name": name,
                "Price": price,
                "Change": change,
                "Change%": change_perc,
                "Volume": volume,
                "50-day-avg": fiftydayavg,
                "200-day-avg": twohundreddayavg,
            }
            yahoolist.append(yahoo)
    else:
        print("Parsing failed.")
    return yahoolist


def main():
    """This is the main function where we can input the url, 
    call our functions and parse HTML data into a pandas dataframe."""

    # Parsing trending ETFs on yahoo finance
    url = "https://finance.yahoo.com/markets/etfs/trending/"
    parse = extract(url)
    if parse:
        yahoolist = transform(parse)
        df = pd.DataFrame(yahoolist)
        print(df)


if __name__ == "__main__":
    main()
