import json
import requests
from log import LOG


def query_openrouter(prompt):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer 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",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "openai/gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                    ]
                }
            ],

        })
    )
    try:
        return response.json()["choices"][0]["message"]["content"]
    except:
        LOG("Something went wrong.")
        LOG("prompt: ", prompt)
        LOG("response: ", response.json())
        LOG("Retrying...")
        return query_openrouter(prompt)


def generate_short_description(text, language_name):

    prompt = f"""
    Below is webscraped content from various sources about {language_name}.
    Generate a concise summary based ONLY on these sources (max 5 sentences). Use Markdown. In your summary, 
    don't mention the sources themselves. 
    Content:
    {text}
    """

    return query_openrouter(prompt)


def generate_long_description(text, language_name):

    prompt = f"""
    Below is webscraped content from various sources about {language_name}.
    Generate an informative summary based ONLY on these sources. Max one A4 page long.
    Use Markdown. At the very end of the article, put sources (only useful links). Instead of raw links,
    put aliases displaying name of the website (e.g. wikipedia instead of www.wikipedia.org), redirecting to the source.
    All links should be in smaller font than the rest. There might be sources in other languages. 
    Remember to write everything in English.
    Don't add any title e.g. "{language_name} overwiew". I will add the title manually.
    Scraped Content:
    {text}
    Long Description:
    """

    return query_openrouter(prompt)


def generate_markdown_from_ready_text(text):
    prompt = f"""
        Below is some text. Generate a readable, nice-looking Markdown version of it.
        Content:
        {text}
        Long Description:
        """

    return query_openrouter(prompt)
