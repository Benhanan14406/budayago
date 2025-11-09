from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from modules.main.models import UserProfile, DailyStreak
from django.shortcuts import get_object_or_404
from .serializers import UserProfileSerializer
import uuid
from datetime import  timedelta
from django.utils import timezone

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Ensure the profile is created for the authenticated user
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def me(self, request):
        # Endpoint to get current user's profile
        profile = self.get_queryset().first()
        if not profile:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request, *args, **kwargs):
        profile = self.get_queryset().first()
        if not profile:
            return Response(
                {"detail": "Profile not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        partial = request.method == 'PATCH'
        serializer = self.get_serializer(
            profile, 
            data=request.data, 
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'])
    def delete(self, request):
        """Delete current user's profile"""
        profile = self.get_queryset().first()
        if not profile:
            return Response(
                {"detail": "Profile not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        user = profile.user
        user.delete()
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['post'])
    def start_session(self, request, email=None):
        session_id = str(uuid.uuid4())
        return Response({"session_id": session_id})
    
    @action(detail=False, methods=['post'])
    def end_session(self, request,  email=None):
        profile = self.get_queryset().first()
        session_id = request.data.get('session_id')
        start_time_str = request.data.get('start_time')
        end_time_str = request.data.get('end_time')

        if not all ([session_id, start_time_str, end_time_str]):
            return Response({"error": "missing session, start_time, or end_time"}, status=400)
        
        try:
            start_time = timezone.datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
            end_time = timezone.datetime.fromisoformat(end_time_str.replace('Z', '+00:00'))
        except ValueError:
            return Response({"error": "Invalid time format"}, status=400)
        
        if end_time <= start_time:
            return Response({"error": "End time must be after start time"}, status=400)
        
        duration = int((end_time - start_time).total_seconds()/60)
        today = timezone.now().date()

        streak, created = DailyStreak.objects.get_or_create(
            user=profile, date=today, defaults={'total_minutes': 0}
        )
        streak.total_minutes += duration
        streak.save()
        
        if streak.total_minutes >= 5 and profile.last_streak_date != today:
            if profile.last_streak_date and today > profile.last_streak_date + timedelta(days=1):
                profile.streak = 0
            profile.streak += 1
            profile.last_streak_date = today
            profile.save()

        return Response({'total_minutes_today': streak.total_minutes, "streak": profile.streak})
    




        
