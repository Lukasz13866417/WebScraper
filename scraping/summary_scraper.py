import json
import requests
from log import LOG


def query_openrouter(prompt):
    """
    Sends a query to OpenRouter API and returns the response.
    """
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer sk-or-ghjghjghjghjghjghjghjgjghjghjgjh",
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
    Below is collected content from various sources about {language_name}.
    Generate a concise summary based on these sources (max 3 sentences). Use Markdown.
    Content:
    {text}
    """

    return query_openrouter(prompt)


def generate_long_description(text, language_name):

    prompt = f"""
    Below is collected content from various sources about {language_name}.
    Generate a single concise and informative summary based on these sources (max 20 sentences).
    Use Markdown.
    At the very end, add links to the original source. Maybe they should be in smaller font than the rest.
    Content:
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
