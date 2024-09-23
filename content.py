import openai
import os

def authenticate_openai_api():
    openai.api_key = "<YOUR_OPENAI_API_KEY_HERE>"

def read_research_file(topic):
    filename = f"{topic.replace(' ', '_')}_research.txt"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    else:
        print(f"Research file {filename} not found.")
        return ""

def generate_case_study_chunked(research_content, topic):
    sections = [
        # Replace with appropiate sections for your project
        "Introduction",
        "Historical Context",
        "Current Implementations",
        "Impact",
        "Future Considerations",
        "Conclusion",
        "References"
    ]
    case_study_content = ""

    for section in sections:
        try:
            prompt_content = f"Using the following research data, generate the **{section}** section for a comprehensive and detailed case study on {topic}. The section should be written in a cohesive paragraph format without subsections:\n\n{research_content}"
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are tasked with creating a detailed and comprehensive case study based on the provided research content."
                    },
                    {
                        "role": "user",
                        "content": prompt_content
                    }
                ],
                max_tokens=2048,
                temperature=0.7,
            )
            chunk_content = response.choices[0].message['content'].strip()
            case_study_content += f"\n\n### {section} ###\n\n" + chunk_content + "\n\n"
            print(f"Processed section {section} successfully.")
        except Exception as e:
            print(f"Error generating content for section {section}: {e}")

    return case_study_content

def save_case_study_to_file(content, topic):
    filename = f"{topic.replace(' ', '_')}_case_study_content.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Case study content saved to {filename}")


topic = "TOPIC NAME"

# Authenticate OpenAI API
authenticate_openai_api()

# Read research data
research_content = read_research_file(topic)

# Generate and save detailed case study
if research_content:
    case_study_content = generate_case_study_chunked(research_content, topic)
    save_case_study_to_file(case_study_content, topic)
