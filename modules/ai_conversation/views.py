# myapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import get_gemini_response, get_tts_response, transcribe_audio
from .const import DUMMY_USER

class GeminiChatView(APIView):
    def post(self, request, *args, **kwargs):
        language = request.data.get("bahasa", "")
        user_prompt = request.data.get('prompt', '')
        history = request.session.get('chat_history', [])

        if not user_prompt:
            return Response({'error': 'No prompt provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Call the LangChain service
        ai_response = get_gemini_response(user_prompt, language, DUMMY_USER, chat_history=history)
        get_tts_response(ai_response)

        history.append(("human", user_prompt))
        history.append(("ai", ai_response))
        request.session["chat_history"] = history
        request.session.modified = True
        
        return Response({'response': ai_response}, status=status.HTTP_200_OK)