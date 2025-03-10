"""
import time
import random
from googlesearch import search
from log import LOG
from scraping.general_scraper import scrape_text

UNREADABLE_CONTENT = ["azure","aws",".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"]

def search_google(query, max_results=2):


    try:
        sleep_time = random.uniform(10, 20)
        LOG(f"Sleeping for {sleep_time:.2f} seconds before searching...")
        time.sleep(sleep_time)

        res = ""
        good_texts = 0

        for result in search(query, stop=4):
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
        LOG(f"Error fetching Google Search results: {e}")
        return []

"""
import time
import random
import requests
from log import LOG
from scraping.general_scraper import scrape_text

UNREADABLE_CONTENT = ["azure", "aws", ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"]

# Replace with your actual API Key and Search Engine ID
GOOGLE_API_KEY = "AIzaSyCAel_Ae7O-cMhMHPEKIqfhsu04vQ3QJC4"
GOOGLE_CSE_ID = "373d807ac0c8e48e5"


def google_search_api(query, stop=4):
   
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": query,
            "key": GOOGLE_API_KEY,
            "cx": GOOGLE_CSE_ID,
            "num": stop
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json().get("items", [])
        return [item["link"] for item in results if "link" in item]
    except Exception as e:
        LOG(f"Error using Google Search API: {e}")
        return []


def search_google(query, max_results=2):
    
    try:
        #sleep_time = random.uniform(10, 20)
        #LOG(f"Sleeping for {sleep_time:.2f} seconds before searching...")
        #time.sleep(sleep_time)

        res = ""
        good_texts = 0

        for result in google_search_api(query, stop=4):
            if any(blocked in result for blocked in UNREADABLE_CONTENT):
                continue  # Skip problematic websites
            LOG("Found url: " + result)
            text = scrape_text(result)
            if text:
                LOG("GOOD TEXT FOUND")
                good_texts += 1
                res += f"SOURCE: {result}\n{text} \n\n"
                if good_texts >= max_results:
                    break

        return res

    except Exception as e:
        LOG(f"Error fetching Google Search results: {e}")
        return ""


#print(search_google("Python programming language advantages"))
