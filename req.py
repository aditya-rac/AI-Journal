import requests

def authenticate_api():
    return "<YOUR_API_KEY_HERE>"

def send_to_perplexity(messages, model="llama-3.1-sonar-large-128k-chat"):
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

def explain_requirements_for_case_study(topic):
    messages = [
        {
            "role": "system",
            "content": "You are tasked with creating a detailed and specific case study for <specific topic you want to ask for>"
        },
        {
            "role": "user",
            "content": f'''
            Please generate a comprehensive and detailed case study based on the following requirements:
            - Include quotes from key figures relevant to the topic.
            - Provide a thorough analysis of {topic}, including historical context, current implementations, and future considerations.
            - Discuss the impact of the topic in detail, including social, economic, or technical factors.
            - Highlight key projects, collaborations, or innovations associated with {topic}.
            - Ensure the content is highly specific, detailed, and relevant to the subject matter.
            - Include all sources and resources used at the end of the document.
            '''
        }
    ]

    response = send_to_perplexity(messages, "llama-3.1-sonar-large-128k-chat")
    explanation_content = response.get('choices', [{}])[0].get('message', {}).get('content', "")
    return explanation_content

# Example usage:
topic = "The Rise of AI in the 2020s"
explanation_content = explain_requirements_for_case_study(topic)

# Save the requirements explanation to a file
with open(f"{topic.replace(' ', '_')}_requirements_explanation.txt", "w", encoding="utf-8") as file:
    file.write(explanation_content)

print(f"Requirements explanation saved to {topic.replace(' ', '_')}_requirements_explanation.txt")
