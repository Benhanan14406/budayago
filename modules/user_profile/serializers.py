from rest_framework import serializers
from modules.main.models import UserProfile, Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'base_language', 'target_language']

class UserProfileSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)
    current_course = CourseSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'user',
            'email', 'name', 'age', 'region',
            'courses', 'current_course', 'xp', 'level', 'gems',
            'last_login', 'created_at', 'updated_at'
        ]
        read_only_fields = ['email', 'created_at', 'updated_at', 'last_login']

    # def create(self, validated_data):
    #     # Handle creation, ensure user is linked
    #     user = self.context['request'].user
    #     validated_data['user'] = user
    #     return super().create(validated_data)