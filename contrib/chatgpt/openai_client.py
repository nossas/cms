from django.conf import settings
import openai

openai.api_key = settings.OPENAI_SECRET_KEY

def answer_me(text: str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a chatbot"},
                {"role": "user", "content": text},
            ]
    )

    result = ''
    for choice in response.choices:
        result += choice.message.content

    return result