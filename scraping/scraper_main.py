import os

from log import LOG
from scraping.openrouter import generate_long_description
from scraping.google_scraper import search_google
from scraping.openrouter import generate_short_description
from langinfo import LangInfo

def get_language_info(lang_metadata_list):

    lang_info_list = []

    for lang in lang_metadata_list:
        LOG(f"Searching for info on: {lang.name}...")

        # Fetch URLs from Google
        text_from_urls = search_google(f"{lang.name} programming language")
        text_from_urls += search_google(f"{lang.name} programming language criticism")
        text_from_urls += search_google(f"{lang.name} programming language advantages")
        text_from_urls += search_google(f"{lang.name} programming language uses")
        #text_from_urls += search_google(f"{lang.name} programming language key features")

        short_description = generate_short_description(text_from_urls,lang.name)
        long_description = generate_long_description(text_from_urls,lang.name)

        lang_info = LangInfo(lang, short_description, long_description)
        lang_info_list.append(lang_info)

    return lang_info_list

def save_to_file(lang_info_list, filename=os.path.join(os.path.dirname(__file__), "..", "data", "scraped_languages.txt")):

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as file:
        for lang_info in lang_info_list:
            file.write(str(lang_info) + "\n")
            file.write("=" * 80 + "\n")

    LOG(f"Data saved to {os.path.abspath(filename)}")

def load_from_file(filename=os.path.join(os.path.dirname(__file__), "..", "data", "scraped_languages.txt")):

    lang_info_list = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
            lang_entries = content.strip().split("=" * 80)

            for entry in lang_entries:
                entry = entry.strip()
                if entry:
                    lang_info_list.append(LangInfo.from_string(entry))

        LOG(f"Data loaded from {os.path.abspath(filename)}")
    except FileNotFoundError:
        LOG("File not found. Please run the scraper first.")
    except Exception as e:
        LOG(f"Error reading file: {e}")

    return lang_info_list