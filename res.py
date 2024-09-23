import requests
import os

def authenticate_api():
    return "<YOUR_API_KEY_HERE>"

def send_to_perplexity(messages, model="llama-3.1-sonar-small-128k-online"):
    print(f"Sending request to Perplexity using model {model}...")
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {authenticate_api()}"
    }
    payload = {
        "model": model,
        "messages": messages
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error communicating with Perplexity API: {e}")
        return {}

def gather_research_for_topic(topic):
    # Read the requirements explanation
    filename = f"{topic.replace(' ', '_')}_requirements_explanation.txt"
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return ""

    with open(filename, "r", encoding="utf-8") as file:
        requirements_explanation = file.read()

    urls = [
        "<URL_1>",
        "<URL_2>"
    ]

    research_content = ""
    references_content = ""
    for url in urls:
        messages = [
            {
                "role": "system",
                "content": requirements_explanation
            },
            {
                "role": "user",
                "content": f"Please provide comprehensive research and insights based on the article found at: {url}. If the URL is not accessible, perform in-depth personal research on the topic."
            }
        ]

        response = send_to_perplexity(messages, "llama-3.1-sonar-small-128k-online")
        content = response.get('choices', [{}])[0].get('message', {}).get('content', "")
        if not content:
            print(f"URL {url} did not return content. Performing personal research.")
            messages = [
                {
                    "role": "system",
                    "content": requirements_explanation
                },
                {
                    "role": "user",
                    "content": f"Please perform in-depth personal research and provide comprehensive insights on {topic}, including quotes, projects, and impacts."
                }
            ]
            response = send_to_perplexity(messages, "llama-3.1-sonar-small-128k-online")
            content = response.get('choices', [{}])[0].get('message', {}).get('content', "")
        
        # Append the content and the URL (reference) to the research and references
        research_content += content + "\n\n"
        references_content += f"Reference: {url}\n"

    return research_content, references_content

def save_research_and_references_to_files(research_content, references_content, topic):
    # Save the research data
    research_filename = f"{topic.replace(' ', '_')}_research.txt"
    with open(research_filename, "w", encoding="utf-8") as file:
        file.write(research_content)
    print(f"Research data saved to {research_filename}")

    # Save the references (URLs)
    references_filename = f"{topic.replace(' ', '_')}_references.txt"
    with open(references_filename, "w", encoding="utf-8") as file:
        file.write(references_content)
    print(f"References saved to {references_filename}")

# Example usage:
topic = "The Rise of AI in the 2020s"
research_content, references_content = gather_research_for_topic(topic)
if research_content:
    save_research_and_references_to_files(research_content, references_content, topic)
