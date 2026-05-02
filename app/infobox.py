from fastapi import APIRouter
import requests
import re
from bs4 import BeautifulSoup

router = APIRouter()

def get_infobox(search_term):

    url = f"https://en.wikipedia.org/wiki/{search_term}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36u "
    }

    response = requests.get(url, headers=headers)

    html = response.text

    soup = BeautifulSoup(html, "html.parser")

    infobox = soup.find("table", {"class": "infobox"})

    rows = infobox.find_all("tr")

    data = {}

    for row in rows:
        header = row.find("th")
        value = row.find("td")
        
        if header and value:
            data[header.get_text(strip=True)] = value.get_text(strip=True)

    clean_data = {}

    for key, value in data.items():
        clean_key = re.sub(r"\xa0", " ", key)
        clean_value = re.sub(r"\xa0", " ", value)
        
        clean_data[clean_key.strip()] = clean_value.strip()

    return clean_data

@router.get("/infobox")
def infobox(search_term):
    result = get_infobox(search_term)
    return result