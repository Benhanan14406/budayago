from django.shortcuts import render
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from django.conf import settings
from .const import JAWA_PRE_PROMPT, SUNDA_PRE_PROMPT

# Create your views here.
def get_user_context(user_profile):
    courses_str = ", ".join(user_profile.get("courses", []))

    user_context = f"""
    [INFORMASI PENGGUNA]
    Nama: {user_profile.get('name', 'Pengguna')} ({user_profile.get('username')})
    Usia: {user_profile.get('age', '-')} tahun
    Asal: {user_profile.get('region', '-')}
    Status Belajar: Level {user_profile.get('level', 1)}, XP {user_profile.get('xp', 0)}
    Kursus Aktif: {user_profile.get('current_course', '-')}
    Riwayat Kursus: {courses_str}
    Streak: {user_profile.get('streak', 0)} hari
    
    Gunakan informasi ini untuk mempersonalisasi jawabanmu.
    """
    return user_context

def get_gemini_response(user_prompt, bahasa, user_profile,chat_history=[]):
    gemini = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.7
    )
    
    ai_language = ""
    if bahasa.lower() == "sunda":
        ai_language = SUNDA_PRE_PROMPT
    else:
        ai_language = JAWA_PRE_PROMPT

    messages = [
        ("system", ai_language + "\n" + get_user_context(DUMMY_USER)),
    ]

    for msg in chat_history:
        if isinstance(msg, list):
            messages.append(tuple(msg))
        else:
            messages.append(msg)
            
    messages.append(("human", "{user_input}"))
    prompt_template = ChatPromptTemplate.from_messages(messages) 
    chain = prompt_template | gemini | StrOutputParser()

    try:
        response = chain.invoke({"user_input": user_prompt})
        return response
    except Exception as e:
        return f"Error Connecting to Gemini: {str(e)}"
