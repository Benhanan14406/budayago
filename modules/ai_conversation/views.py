# myapp/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .services import get_gemini_response

@method_decorator(csrf_exempt, name='dispatch')
class GeminiChatView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_prompt = data.get('prompt', '')

            if not user_prompt:
                return JsonResponse({'error': 'No prompt provided'}, status=400)

            # Call the LangChain service
            ai_response = get_gemini_response(user_prompt)

            return JsonResponse({'response': ai_response})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)