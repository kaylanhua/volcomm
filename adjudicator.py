import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

COMPANY_NAME = "Palantir"

# Set up OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def split_content(content):
    return content.split('--------------------------------------------------')

def create_prompt(sections):
    prompts = []
    current_prompt = "For each of the following requirements, evaluate whether {COMPANY_NAME} fulfills the voluntary commitment based on the provided information. Rate each requirement as 0 (not fulfilled), 0.5 (partially fulfilled), or 1 (fully fulfilled). Disregard any links. Here are the requirements and corresponding information:\n\n"
    
    for i, section in enumerate(sections, 1):
        if section.strip():
            current_prompt += section.strip() + "\n\n"
        
        if i % 10 == 0 or i == len(sections):
            current_prompt += "Please provide your evaluation for each requirement in the format:\n"
            current_prompt += "Requirement: [Requirement text]\n"
            current_prompt += "Rating: [0/0.5/1]\n"
            current_prompt += "Explanation: [Brief explanation]\n\n"
            prompts.append(current_prompt)
            current_prompt = "Continuing from the previous evaluation, please assess the following requirements:\n\n"
    
    return prompts

def query_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI expert tasked with evaluating a company's fulfillment of voluntary AI commitments."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,
        n=1,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()

def main():
    content = read_file(f'{COMPANY_NAME}_final.txt')
    sections = split_content(content)
    prompts = create_prompt(sections)
    
    all_evaluations = []
    for i, prompt in enumerate(prompts, 1):
        print(f"Processing batch {i} of {len(prompts)}...")
        evaluation = query_gpt(prompt)
        all_evaluations.append(evaluation)
    
    with open(f'{COMPANY_NAME}_scores.txt', 'w', encoding='utf-8') as file:
        file.write("\n\n".join(all_evaluations))
    
    print("Evaluation complete. Results saved in {COMPANY_NAME}_scores.txt")

if __name__ == "__main__":
    main()
