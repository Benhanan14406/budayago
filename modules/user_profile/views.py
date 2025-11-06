from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from modules.main.models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # permission_classes = [IsAuthenticated]
    lookup_field = 'email'  # Use email as lookup since it's the primary key

    # def get_queryset(self):
    #     # Users can only see their own profile
    #     return UserProfile.objects.filter(user=self.request.user)

    # def perform_create(self, serializer):
    #     # Ensure the profile is created for the authenticated user
    #     serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def me(self, request):
        # Endpoint to get current user's profile
        profile = self.get_queryset().first()
        if not profile:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # Custom update to handle partial updates
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
