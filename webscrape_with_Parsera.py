# Using a new lightweight python library called Parsera that utilizes LLMs to scrape websites making web scraping a very easy 
# & straight-forward task. I scraped a few different websites and pulled the results in a json file with ease using pandas. I 
# needed OpenAI API key & some usage credit to make requests. Parsera pulls all the data and uses LLM(gpt-4o in this case) to
# figure out the columns requested. The library works with dynamic websites & can scroll pages as well.

import os
from parsera import Parsera
import pandas as pd


url = "https://finance.yahoo.com/markets/world-indices/"
elements = {
    "Symbol": "Symbol",
    "Name": "Stock Name",
    "Price": "Price",
    "Change": "Change",
    "Change%": "Change%",
    "Volume": "Volume",
}

scraper = Parsera()
result = scraper.run(url=url, elements=elements)

df = pd.DataFrame(result)
print(df)

df_json = df.to_json("yahoo-output.json", orient="records", lines=True)
