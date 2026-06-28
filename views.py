from django.shortcuts import render
from django.http import JsonResponse
import re 
from openai import OpenAI
import os

def get_response(user_input):
    response = OpenAI.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )
    return response['choices'][0].message.content

# ---------- PAGE LOAD ----------
def index(request):
    return render(request, 'chat/index.html')


# ---------- TEXT CLEANER ----------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)  # remove punctuation
    return text.strip()


# ---------- CHATBOT LOGIC ----------
def get_response(request):
    if request.method == "POST":

        user_msg = request.POST.get('message', '')
        cleaned_msg = clean_text(user_msg)

        # session memory
        last_answer = request.session.get('last_answer')

        knowledge = {
            "capital of india": "New Delhi is the capital of India.",
            "president of india": "The President of India is Droupadi Murmu.",
            "prime minister of india": "The Prime Minister of India is Narendra Modi.",
        }

        # WHY handling
        if cleaned_msg in ["why", "explain"]:
            if last_answer:
                bot_reply = "Here's why: " + last_answer+ "Im a learning agent you can also teach me why this can be the answer."
            else:
                bot_reply = "Why about what? Please ask something first."

        else:
            bot_reply = "That sounds interesting. Can you ask in a different way?"

            for key in knowledge:
                if key in cleaned_msg:
                    bot_reply = knowledge[key]
                    request.session['last_answer'] = bot_reply
                    break

        return JsonResponse({"reply": bot_reply})

    return JsonResponse({"reply": "Invalid request"})
