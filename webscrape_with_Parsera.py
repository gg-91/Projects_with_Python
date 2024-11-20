import os
from parsera import Parsera
import pandas as pd


url = "https://www.indeed.com/jobs?q=data+analyst&l=San+Francisco%2C+CA"
elements = {
    "Title": "Job title",
    "Company": "Company name",
    "Location": "Job location",
    "Full job description": "Job Description",
}

scraper = Parsera()
result = scraper.run(url=url, elements=elements)

df = pd.DataFrame(result)
print(df)

df_json = df.to_json("Indeed-out.json", orient="records", lines=True)
