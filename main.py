from scraping.scraper_main import save_to_file, load_from_file
from scraping.summary_scraper import generate_markdown_from_ready_text


def main():
    from scraping.scraper_main import get_language_info
    from scraping.tiobe_scraper import scrapeTIOBE
    from markdown.pagemaker import build_front_page, build_list_page, build_language_page
    from log import LOG

    LOG("Starting. Scraping TIOBE")
    tiobe_data = scrapeTIOBE()
    LOG("TIOBE data scraped")

    basic_info = generate_markdown_from_ready_text(tiobe_data["basic info"])
    LOG("Basic info scraped: \n", basic_info)

    languages = tiobe_data["languages"]
    LOG("Language list scraped: \n")
    for lang in languages:
        LOG(str(lang))

    LOG("Searching for detailed info about languages")
    lang_info = get_language_info(languages)
    save_to_file(lang_info)
    LOG("Detailed info scraped")

    LOG("Building pages")
    LOG("Building front page")
    build_front_page(basic_info)

    LOG("Building list page")
    build_list_page(lang_info)

    for lang in lang_info:
        LOG(f"Building language page for {lang.metadata.name}")
        build_language_page(lang)

    LOG("Done.")


if __name__ == "__main__":
    main()