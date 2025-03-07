import traceback
import requests
from log import LOG

UNREADABLE_CONTENT = ["azure","aws",".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"]

import re
from bs4 import BeautifulSoup

def clean_text(text):
    """
    Cleans the text by:
    - Removing common ad-like or boilerplate phrases.
    - Stripping all HTML tags.

    :param text: The input text to clean.
    :return: The cleaned text.
    """
    if not text or not isinstance(text, str):
        return ""

    # Remove HTML tags
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text(separator=" ")  # Keeps readable spacing

    # Common ad-like phrases to remove
    ad_like_phrases = [
        "click here", "terms of service", "privacy policy", "subscribe now",
        "all rights reserved", "copyright", "contact us", "cookies policy",
        "advertisement", "sponsored", "sign up for free", "get started now"
    ]

    text_lower = text.lower()

    for phrase in ad_like_phrases:
        if phrase in text_lower:
            # Use regex to remove the phrase (case-insensitive)
            text = re.sub(rf"\b{re.escape(phrase)}\b", "", text, flags=re.IGNORECASE)

    return text.strip()



def is_good(text):
    """
    Checks if a given text is suitable for analysis.

    :param text: The text to analyze.
    :return: True if the text is good, False otherwise.
    """
    if text is None or not isinstance(text, str):
        return False

    text = text.strip()

    # Remove ad-like content first
    text = clean_text(text)

    # Reject empty or excessively short/long texts
    if len(text) < 300:
        LOG("Text too short. Skipping...")
        return False

    # Reject texts that are mostly non-alphabetic (likely code, spam, or random data)
    special_chars_ratio = len(re.findall(r"[^a-zA-Z\s]", text)) / len(text)
    if special_chars_ratio > 0.4:
        LOG("Text contains mostly non-alphabetic characters. Skipping...")
        return False

    # Reject texts that are mostly numbers
    digit_ratio = len(re.findall(r"\d", text)) / len(text)
    if digit_ratio > 0.3:
        LOG("Text contains mostly numbers. Skipping...")
        return False

    # Reject texts that are mostly uppercase
    uppercase_ratio = len(re.findall(r"[A-Z]", text)) / len(text)
    if uppercase_ratio > 0.6:
        LOG("Text contains mostly uppercase characters. Skipping...")
        return False

    # Reject texts with excessive line breaks
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
        LOG(f"🌍 Scraping content from: {url}")

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract text, remove scripts and styles
        for tag in soup(["script", "style", "noscript"]):
            tag.extract()

        text = soup.get_text(strip=True)
        if is_good(text):
            return clean_text(text)
        else:
            raise Exception(f"Text from {url} is most likely garbage.")

    except Exception as e:
        # Get full stack trace and log it
        error_trace = traceback.format_exc()
        LOG(f"❌ Error fetching content from {url}:\n{error_trace}")
        return None
