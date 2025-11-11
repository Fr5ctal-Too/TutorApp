from google import genai
from credentials import gemini


client = genai.Client(api_key=gemini)


def generate_question(topic):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f'Generate a question about the following topic: {topic}. You only have to give the question statement and nothing else. Question statement: ',
    )
    return response.text
