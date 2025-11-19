from django.shortcuts import render
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from django.conf import settings
from .const import JAWA_PRE_PROMPT, SUNDA_PRE_PROMPT
import scipy
from modules.ai_conversation.const import JAWA_PRE_PROMPT, SUNDA_PRE_PROMPT
from transformers import VitsModel, AutoTokenizer, Wav2Vec2ForCTC, Wav2Vec2Processor
import torchaudio 
import torch
import os

# stt_model = whisper.load_model("tiny")

wav2vec_processor = Wav2Vec2Processor.from_pretrained("indonesian-nlp/wav2vec2-indonesian-javanese-sundanese")
wav2vec_model = Wav2Vec2ForCTC.from_pretrained("indonesian-nlp/wav2vec2-indonesian-javanese-sundanese")

wav2vec_resampler = torchaudio.transforms.Resample(48_000, 16_000)

gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0.7
)

tts_model = VitsModel.from_pretrained("facebook/mms-tts-ind")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-ind")

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
    
    ai_language = ""
    if bahasa.lower() == "sunda":
        ai_language = SUNDA_PRE_PROMPT
    else:
        ai_language = JAWA_PRE_PROMPT

    messages = [
        ("system", ai_language + "\n" + get_user_context(user_profile)),
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
    

def get_tts_response(gemini_response):
    """
    Converts text to speech, saves it to a static file, and returns the URL path.
    """
    text = gemini_response
    inputs = tokenizer(text, return_tensors="pt")

    with torch.no_grad():
        output = tts_model(**inputs).waveform

    # NOTE: For a real application, you would save this to a unique filename
    # and handle media file storage properly. For this boilerplate, we'll
    # overwrite the same file in the static directory.
    output_path = "static/audio/response.wav"
    output_url = "/static/audio/response.wav"
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    scipy.io.wavfile.write(output_path, rate=tts_model.config.sampling_rate, data=output.squeeze().cpu().numpy())
    
    return output_url

# def transcribe_audio(audio_file):
#     try:
#         audio = whisper.load_audio(audio_file)
#         audio = whisper.pad_or_trim(audio)
#         mel = whisper.log_mel_spectrogram(audio, n_mels=stt_model.dims.n_mels).to(stt_model.device)

#         # detect the spoken language
#         _, probs = stt_model.detect_language(mel)
#         print(f"Detected language: {max(probs, key=probs.get)}")

#         # decode the audio
#         options = whisper.DecodingOptions()
#         result = whisper.decode(stt_model, mel, options)

#         # print the recognized text
#         print(result.text)
#     except Exception as e:
#         print(f"Error during transcription: {e}")
#         return None


def transcribe_audio(audio_file):
    try:
        speech_array, sampling_rate = torchaudio.load(audio_file)

        if sampling_rate != 16_000:
            print(f"Resampling audio dari {sampling_rate}Hz ke 16000Hz...")
            speech_array = wav2vec_resampler(speech_array)

        inputs = wav2vec_processor(speech_array.squeeze().numpy(), sampling_rate=16_000, return_tensors="pt", padding=True)

        with torch.no_grad():
            logits = wav2vec_model(inputs.input_values, attention_mask=inputs.attention_mask).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = wav2vec_processor.batch_decode(predicted_ids)

        return transcription[0]
    except Exception as e:
        print(f"Error during Wav2Vec2 transcription: {e}")
        return None
