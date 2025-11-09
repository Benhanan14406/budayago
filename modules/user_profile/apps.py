from django.apps import AppConfig


class UserProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_profile'

    def ready(self):
        from django.db.models.signals import post_save
        from django.dispatch import receiver
        from django.contrib.auth.models import User
        from modules.main.models import UserProfile

        @receiver(post_save, sender=User)
        def create_user_profile(sender, instance, created, **kwargs):
            if created or not hasattr(instance, 'userprofile'):
                UserProfile.objects.create(
                    user=instance,
                    email=instance.email,
                    name=f"{instance.first_name} {instance.last_name}".strip() or instance.username,
                )
