import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

from log import LOG

def find_reddit_meme(language):
    if language == "Go":
        language = "Golang"
    if "Delphi" in language:
        language = "Object Pascal"

    # Encode the string (handling special characters like C++ and C#)
    encoded_language = quote(language)
    search_url = f"https://www.reddit.com/search/?q={encoded_language}%20programming%20meme&sort=relevance&t=all"
    if language == "R":
        search_url = f"https://www.reddit.com/search/?q=RStudio%20meme&sort=relevance&t=all"
    if language == "Prolog":
        search_url = f"https://www.reddit.com/search/?q=programming%20in%20prolog%20meme&sort=relevance&t=all"
    if language == "Assembly":
        search_url = f"https://www.reddit.com/search/?q=programming%20in%20Assembly%20meme&sort=relevance&t=all"

    headers = {'User-Agent': 'Mozilla/5.0'}
    print(search_url)
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        LOG("Failed to fetch reddit search results.")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Look for post links. They have certain data attributes
    post_links = []
    for link in soup.find_all('a', {'data-testid': 'post-title'}, href=True):
        href = link['href']
        post_links.append((href, link.text.strip()))

    # Check for valid posts with the exact language name
    for post_link, post_title in post_links:
        full_post_url = f"https://www.reddit.com{post_link}.json"

        post_response = requests.get(full_post_url, headers=headers)
        if post_response.status_code != 200:
            continue

        post_json = post_response.json()

        images = []
        try:
            for item in post_json[0]['data']['children']:
                media_metadata = item['data'].get('media_metadata', {})
                if media_metadata:
                    for key, img_data in media_metadata.items():
                        if 's' in img_data and 'u' in img_data['s']:
                            images.append(img_data['s']['u'].replace('&amp;', '&'))

                preview = item['data'].get('preview', {}).get('images', [])
                for img in preview:
                    source_url = img.get('source', {}).get('url', '').replace('&amp;', '&')
                    if source_url:
                        images.append(source_url)
        except (KeyError, IndexError):
            continue

        if images:
            return images[0], f"https://www.reddit.com{post_link}"

    LOG("No suitable meme found.")
    return None


language = "Assembly"
meme_image_url = find_reddit_meme(language)
if meme_image_url:
    print("Meme found:", meme_image_url)
    print(f"Markdown link: ![Meme]({meme_image_url})")
else:
    print("No meme found.")



