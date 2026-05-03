import httpx
import re
from bs4 import BeautifulSoup
from urllib.parse import quote
from fastapi import APIRouter

router = APIRouter()

async def search_helper(search_term, limit=20):

    search_term = quote(search_term)
    url = f"https://en.wikipedia.org/w/index.php?limit={limit}&fulltext=1&ns0=1&search={search_term}&title=Special%3ASearch&profile=default"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36'
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    html = response.text

    titles = BeautifulSoup(html, "html.parser").find_all("div", {"class": "mw-search-result-heading"})

    links = []

    for tag in titles:
        htmls = str(tag)
        matches = re.findall(r'href="/wiki/([^"]+)"', htmls)
        matches = [re.sub(r'%[0-9A-Fa-f]{2}', "", match) for match in matches]
        links.extend(matches)

    return links

@router.get("/search_helper")
async def searchhelper(search_term: str, limit: int = 20):
    allowed_limits = [20, 50, 100, 250, 500]
    if limit not in allowed_limits:
        return {"error": "Invalid limit. Allowed values are 20, 50, 100, 250, 500."}
    
    results = await search_helper(search_term, limit)
    return {"results": results}