from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, UserPreference


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField()
    
    class Meta:
        model = UserProfile
        fields = [
            'bio', 'avatar', 'date_of_birth', 'age', 'dietary_restrictions',
            'allergies', 'favorite_cuisines', 'disliked_ingredients',
            'cooking_skill_level', 'preferred_meal_time', 'activity_level',
            'weight_goal', 'notifications_enabled', 'meal_reminders',
            'shopping_reminders', 'recipe_recommendations'
        ]


class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = ['id', 'preference_type', 'name', 'preference_score', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']


class UserProfileDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    preferences = UserPreferenceSerializer(source='user.preferences', many=True, read_only=True)
    age = serializers.ReadOnlyField()
    
    class Meta:
        model = UserProfile
        fields = [
            'user', 'bio', 'avatar', 'date_of_birth', 'age', 'dietary_restrictions',
            'allergies', 'favorite_cuisines', 'disliked_ingredients',
            'cooking_skill_level', 'preferred_meal_time', 'activity_level',
            'weight_goal', 'notifications_enabled', 'meal_reminders',
            'shopping_reminders', 'recipe_recommendations', 'preferences',
            'created_at', 'updated_at'
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='userprofile', required=False)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile']
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', None)
        
        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update profile fields
        if profile_data:
            profile = instance.userprofile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError("New passwords do not match.")
        return data
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
