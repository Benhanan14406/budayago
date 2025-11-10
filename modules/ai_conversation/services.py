from django.shortcuts import render
from langchain_google_genai import ChatGoogleGenerativeAI
from django.conf import settings

# Create your views here.

def get_gemini_response(user_prompt):
    gemini = ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.7
    )

    try:
        response = gemini.invoke(user_prompt)
        return response.content
    except Exception as e:
        return f"Error Connecting to Gemini: {str(e)}"
