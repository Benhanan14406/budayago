# myapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import get_gemini_response, get_tts_response, transcribe_audio
from .const import DUMMY_USER
import os
import uuid
from django.conf import settings

class GeminiChatView(APIView):
    """
    A view to handle the full STT -> LLM -> TTS pipeline.
    Accepts an audio file upload and returns AI's text and audio response.
    """
    def post(self, request, *args, **kwargs):
        # 1. Handle Audio Upload
        audio_file = request.FILES.get('audio')
        if not audio_file:
            return Response({'error': 'No audio file provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a temporary file to save the upload
        temp_dir = os.path.join(settings.BASE_DIR, 'temp_audio')
        os.makedirs(temp_dir, exist_ok=True)
        temp_audio_path = os.path.join(temp_dir, f"{uuid.uuid4()}.wav")

        with open(temp_audio_path, 'wb+') as temp_file:
            for chunk in audio_file.chunks():
                temp_file.write(chunk)

        # 2. Speech-to-Text (STT)
        # This will be slow because of the Wav2Vec2 model, as discussed.
        user_prompt = transcribe_audio(temp_audio_path)
        os.remove(temp_audio_path) # Clean up the temporary file

        if user_prompt is None:
            return Response({'error': 'Failed to transcribe audio'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 3. Get LLM Response
        language = request.data.get("bahasa", "jawa") # Default to javanese
        history = request.session.get('chat_history', [])
        
        ai_response_text = get_gemini_response(user_prompt, language, DUMMY_USER, chat_history=history)

        # 4. Text-to-Speech (TTS)
        ai_audio_url = get_tts_response(ai_response_text)

        # Update history
        history.append(("human", user_prompt))
        history.append(("ai", ai_response_text))
        request.session["chat_history"] = history
        request.session.modified = True
        
        # 5. Return final response
        return Response({
            'user_text': user_prompt,
            'ai_text': ai_response_text,
            'ai_audio_url': ai_audio_url
        }, status=status.HTTP_200_OK)