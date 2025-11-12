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

    prompt = 'Strictly predict what the user will ASK next based on this conversation. Do not repeat or evaluate the question. Just give the answer. \n\nConversation History:\n'

    for msg, sender in history:
        if sender == 'own':
            prompt += f'User: {msg}\n'
        elif sender == 'partner':
            prompt += f'Partner: {msg}\n'
        elif sender == 'ai':
            prompt += f'AI: {msg}\n'

    prompt += '\nUser\'s question:'

    return query(prompt)
