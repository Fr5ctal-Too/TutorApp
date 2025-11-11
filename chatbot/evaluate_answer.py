from google import genai
from credentials import gemini


client = genai.Client(api_key=gemini)


def evaluate_answer(question, answer):
    prompt = f'''Evaluate the following answer to the given question.
Provide a score out of 10 and brief feedback.

Question: {question}

Answer: {answer}

Please respond in the following format:
Score: [number from 0-10]
Feedback: [brief feedback on the answer]'''

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )

    response_text = response.text.strip()
    lines = response_text.split('\n')

    score = 0
    feedback = ''

    for line in lines:
        if line.startswith('Score:'):
            try:
                score_str = line.replace('Score:', '').strip()
                score = int(''.join(filter(str.isdigit, score_str.split('/')[0].split('out')[0])))
                score = max(0, min(10, score))
            except:
                score = 0
        elif line.startswith('Feedback:'):
            feedback = line.replace('Feedback:', '').strip()

    if not feedback:
        feedback = '\n'.join([l for l in lines if not l.startswith('Score:')]).strip()

    return {
        'score': score,
        'feedback': feedback
    }
