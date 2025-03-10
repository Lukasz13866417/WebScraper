from scraping.reddit_scraper import find_reddit_meme

def build_front_page(site_info):
    """
    Creates the front page (index.md) with an overview of the project.
    Includes a link to the list of languages.

    :param site_info: Dictionary containing project information.
    """
    content = site_info
    content += "\\[View Language List](languages.md)\n"
    content += "\\[Extra Information](https://www.youtube.com/watch?v=dQw4w9WgXcQ)\n"
    save_markdown("./pages/index.md", content)


def build_list_page(languages):
    """
    Creates a page (`languages.md`) listing all languages with basic information and links to individual pages.

    :param languages: List of LangMetadata objects.
    """
    content = "# Programming Languages\n\n"

    for lang in languages:
        lang_filename = f"{lang.metadata.name.replace(' ', '_')}.md"
        content += f"## [{lang.metadata.name}]({lang_filename})\n"
        content += f"- **Popularity**: {lang.metadata.popularity}\n"
        content += f"- **Rank 2025**: {lang.metadata.rank2025}\n"
        content += f"- **Rank 2024**: {lang.metadata.rank2024}\n"
        content += f"- **Change**: {lang.metadata.change}\n"
        meme,post_url = find_reddit_meme(lang.metadata.name)
        if meme:
            content += f"- [Top meme on Reddit]({post_url})\n\n"
            content += f"![Meme]({meme})"
            content += "\n\n"
        else:
            content += f"No {lang.metadata.name} memes found on Reddit\n\n"

    save_markdown("./pages/languages.md", content)


def build_language_page(lang):
    """
    Creates a markdown page for a specific language.

    :param lang: LangInfo object with metadata, short description, and long description.
    """
    lang_filename = f"{lang.metadata.name.replace(' ', '_')}.md"
    lang_filename = f"{lang_filename.replace('/', '_')}"
    lang_filename = f"{lang_filename.replace('\\', '_')}"

    content = f"# {lang.metadata.name}\n\n"
    content += f"## Overview\n\n{lang.short_description}\n\n"
    content += f"## Detailed Information\n\n{lang.long_description}\n\n"

    save_markdown("./pages/"+lang_filename, content)


def save_markdown(filename, content):
    """
    Saves content to a markdown file, ensuring necessary directories exist.

    :param filename: The path to save the file.
    :param content: The markdown content.
    """
    with open(filename, "w+", encoding="utf-8") as file:
        file.write(content)



#build_list_page([LangInfo(LangMetadata("Fortran",10,10,1,1),"XD","XD")])
