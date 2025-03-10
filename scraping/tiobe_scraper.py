import re
import requests
from bs4 import BeautifulSoup

from langinfo import LangMetadata


url = "https://www.tiobe.com/tiobe-index/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


def scrapeTIOBE():
    # Extract meta information
    paragraphs = soup.find_all("p")
    meta_info = "\n".join([re.sub(r'\s+', ' ', p.text.strip()) for p in paragraphs[2:6]])

    # Extract table data
    languages = []
    table = soup.find("table")  # Find 1st table
    rows = table.find_all("tr")[1:]  # Skip header
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 7:
            rank2025 = int(cols[0].text.strip())
            rank2024 = int(cols[1].text.strip())

            name = cols[4].text.strip()
            popularity = cols[5].text.strip()
            change = cols[6].text.strip()

            lang = LangMetadata(name, popularity, change, rank2025, rank2024)
            languages.append(lang)
    res = dict()
    res["basic info"] = meta_info
    res["languages"] = languages
    return res

"""for lang in scrape()["languages"]:
    LOG(lang)
"""