import requests
from credentials import hf


API_URL = 'https://router.huggingface.co/v1/chat/completions'

headers = {
    'Authorization': f'Bearer {hf}',
}


def query(msg):
    response = requests.post(API_URL, headers=headers, json={
        'messages': [
            {
                'role': 'user',
                'content': msg
            }
        ],
        'model': 'meta-llama/Llama-3.1-8B-Instruct:novita'
    })
    return response.json()['choices'][0]['message']['content']


def follow_up(history):
    if len(history) > 5:
        history = history[-5:]

    prompt = 'Generate stricly one follow-up question with nothing else based on this conversation. There is no need to repeat the question or do any evaluation of the conversation. \n\nConversation History:\n'

    for msg, sender in history:
        if sender == 'own':
            prompt += f'You: {msg}\n'
        elif sender == 'partner':
            prompt += f'Partner: {msg}\n'
        elif sender == 'ai':
            prompt += f'AI: {msg}\n'

    prompt += '\nOnly the Follow-up Response/Question and nothing else:'

    return query(prompt)
