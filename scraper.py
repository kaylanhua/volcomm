import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://api.perplexity.ai/chat/completions"

payload = {
    "model": "llama-3.1-sonar-small-128k-online",
    "messages": [
        {
            "role": "system",
            "content": "Only provide links relevant to this topic."
        },
        {
            "role": "user",
            "content": "What has OpenAI done that might fit under: Establish bounties, contests, or prizes. Make sure to return links used to find this information. Keep it concise and make sure to return all links."
        }
    ],
    "max_tokens": 1000,  # Changed from "Optional" to an integer value
    "temperature": 0.2,
    "top_p": 0.9,
    "return_citations": True,
    "search_domain_filter": ["perplexity.ai"],
    "return_images": False,
    "return_related_questions": False,
    # "search_recency_filter": "year",
    "top_k": 0,
    "stream": False,
    "presence_penalty": 0,
    "frequency_penalty": 1
}
headers = {
    "Authorization": f"Bearer {os.getenv('PPLX_API_KEY')}",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.json()['choices'][0]['message']['content'])