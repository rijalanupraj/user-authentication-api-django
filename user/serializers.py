# External Import
from rest_framework import serializers

# Internal Import
from . import models

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer to Register New User Using CustomUser Model
    """
    password = serializers.CharField(max_length=60, min_length=6, write_only=True)
    username = serializers.CharField(max_length=20, min_length=4)

    class Meta:
        model = models.CustomUser
        fields = ('id','username','email','password')