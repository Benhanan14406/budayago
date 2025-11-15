# myapp/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .services import get_gemini_response
from .const import DUMMY_USER;

@method_decorator(csrf_exempt, name='dispatch')
class GeminiChatView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            language = data.get("bahasa", "")
            user_prompt = data.get('prompt', '')
            history = request.session.get('chat_history', [])

            if not user_prompt:
                return JsonResponse({'error': 'No prompt provided'}, status=400)

            # Call the LangChain service
            ai_response = get_gemini_response(user_prompt, language, DUMMY_USER, chat_history=history)

            history.append(("human", user_prompt))
            history.append(("ai", ai_response))
            request.session["chat_history"] = history
            request.session.modified = True
            return JsonResponse({'response': ai_response})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)