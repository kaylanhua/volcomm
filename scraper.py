import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

url = "https://api.perplexity.ai/chat/completions"
COMPANY_NAME = "Palantir"

headers = {
    "Authorization": f"Bearer {os.getenv('PPLX_API_KEY')}",
    "Content-Type": "application/json"
}

# Read requirements from volcomms.txt
with open('volcomms.txt', 'r') as file:
    requirements = [line.strip() for line in file if line.strip()]

# Open a file to write the results
with open(f'{COMPANY_NAME}_results.txt', 'w') as results_file:
    for requirement in requirements:
        payload = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [
                {
                    "role": "system",
                    "content": "Only provide links relevant to this topic."
                },
                {
                    "role": "user",
                    "content": f"What has {COMPANY_NAME} done that might fit under: {requirement}. Make sure to return links used to find this information. Keep it concise and make sure to return all links."
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.2,
            "top_p": 0.9,
            "return_citations": True,
            "search_domain_filter": ["perplexity.ai"],
            "return_images": False,
            "return_related_questions": False,
            "top_k": 0,
            "stream": False,
            "presence_penalty": 0,
            "frequency_penalty": 1
        }

        max_retries = 3
        retry_delay = 5  # seconds

        for attempt in range(max_retries):
            try:
                response = requests.request("POST", url, json=payload, headers=headers)
                response.raise_for_status()  # Raises an HTTPError for bad responses
                
                content = response.json()
                if 'choices' not in content or not content['choices']:
                    raise KeyError("No 'choices' in the response")
                
                # Write the requirement and response to the file
                results_file.write(f"Requirement: {requirement}\n")
                results_file.write(content['choices'][0]['message']['content'])
                results_file.write("\n\n" + "-"*50 + "\n\n")
                
                # Also print to console for real-time monitoring
                print(f"Processed: {requirement}")
                break  # Success, exit the retry loop
            
            except (requests.RequestException, KeyError, IndexError) as e:
                if attempt < max_retries - 1:
                    print(f"Error processing '{requirement}': {str(e)}. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"Failed to process '{requirement}' after {max_retries} attempts. Skipping.")
                    results_file.write(f"Requirement: {requirement}\n")
                    results_file.write(f"Error: Failed to process after {max_retries} attempts.\n")
                    results_file.write("\n\n" + "-"*50 + "\n\n")

print("All results have been saved to results.txt")