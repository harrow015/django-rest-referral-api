from rest_framework import serializers
from .models import User, Referral


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=20)
    email = serializers.EmailField(max_length=20)
    password = serializers.CharField(max_length=20)
    referral_code = serializers.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ["name", "email", "password", "referral_code"]
        
        
class UserDetailResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "email", "referral_code", "created_at", "referral_points"]

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = ["user", "referred_on"]