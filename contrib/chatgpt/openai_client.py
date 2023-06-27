from django.conf import settings
import openai

openai.api_key = settings.OPENAI_SECRET_KEY

def main():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a chatbot"},
                {"role": "user", "content": "What are the contact emails for federal deputies from the Brazilian Chamber of Deputies?"},
            ]
    )

    result = ''
    for choice in response.choices:
        result += choice.message.content

    print(result)