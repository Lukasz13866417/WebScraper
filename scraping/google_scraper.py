import time
import random
from googlesearch import search

from log import LOG
from scraping.general_scraper import scrape_text

UNREADABLE_CONTENT = ["azure","aws",".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"]

def search_google(query, max_results=3):
    """
    Uses googlesearch to fetch data from URLs for a given query while avoiding garbage websites.
    Includes a delay between searches and rotates user-agents to prevent detection.

    :param query: Search term
    :param max_results: Number of URLs to retrieve (default = 3)
    :return: List of valid URLs
    """

    try:
        # Introduce a random sleep time between requests to mimic human behavior
        sleep_time = random.uniform(6, 10)
        LOG(f"⏳ Sleeping for {sleep_time:.2f} seconds before searching...")
        time.sleep(sleep_time)

        res = ""
        good_texts = 0

        for result in search(query, stop=5):
            if any(blocked in result for blocked in UNREADABLE_CONTENT):
                continue  # Skip problematic websites
            LOG("Found url: "+result)
            text = scrape_text(result)
            if not text is None:
                LOG("GOOD TEXT FOUND")
                good_texts += 1
                if good_texts >= max_results:
                    break
                res += "SOURCE: "+result+"\n"+text + " \n\n"

        return res

    except Exception as e:
        LOG(f"❌ Error fetching Google Search results: {e}")
        return []
