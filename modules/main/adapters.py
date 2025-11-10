from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_login_redirect_url(self, request):
        return '/api/'
    
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        return user