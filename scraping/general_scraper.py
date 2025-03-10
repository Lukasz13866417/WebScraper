import traceback
import requests
from log import LOG
from scraping.openrouter import query_openrouter

UNREADABLE_CONTENT = ["azure", "aws", ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"]

import re
from bs4 import BeautifulSoup

def clean_text(html):
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style", "head", "footer"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def clean_text_further(text):
    prompt = f"""
        Here's some webscraped text. Clean it up. Remove unrelated, ad-like things, irrelevant comments 
        (some comments might be useful though), footers and other things you deem unnecessary.
        Don't change it too much in other ways. Don't include your own comments, as this will be joined with
        similarly scraped&cleaned content and further passed to LLMs.
        The text: \n{text}
    """
    return query_openrouter(prompt)


def is_good(text):
    """
    Checks if a given text is suitable for analysis.
    """
    if text is None or not isinstance(text, str):
        return False

    text = text.strip()

    # Reject empty or excessively short/long texts
    if len(text) < 300:
        LOG("Text too short. Skipping...")
        return False

    special_chars_ratio = len(re.findall(r"[^a-zA-Z\s]", text)) / len(text)
    if special_chars_ratio > 0.4:
        LOG("Text contains mostly non-alphabetic characters. Skipping...")
        return False

    digit_ratio = len(re.findall(r"\d", text)) / len(text)
    if digit_ratio > 0.3:
        LOG("Text contains mostly numbers. Skipping...")
        return False

    uppercase_ratio = len(re.findall(r"[A-Z]", text)) / len(text)
    if uppercase_ratio > 0.6:
        LOG("Text contains mostly uppercase characters. Skipping...")
        return False

    line_break_ratio = text.count("\n") / len(text)
    if line_break_ratio > 0.05:
        LOG("Text contains excessive line breaks. Skipping...")
        return False

    LOG("Text is good. Proceeding...")
    return True  # Passes all filters ✅


def scrape_text(url):
    """
    Scrapes text from a single webpage and returns its content.
    """
    try:
        LOG(f"Scraping content from: {url}")

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        text = response.text
        text = clean_text(text)
        if is_good(text):
            return clean_text_further(text)
        else:
            raise Exception(f"Text from {url} is most likely garbage.")

    except Exception as e:
        # Get full stack trace and log it
        error_trace = traceback.format_exc()
        LOG(f"Error fetching content from {url}:\n{error_trace}")
        return None
