# External Import
from rest_framework import serializers

# Internal Import
from . import models


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer to Register New User Using CustomUser Model
    """
    password = serializers.CharField(
        max_length=60, min_length=6, write_only=True)
    username = serializers.CharField(max_length=20, min_length=4)

    class Meta:
        model = models.CustomUser
        fields = ('id', 'username', 'email', 'password')

    def validate(self, attrs):
        """
        Validating the Data provided by the user by POST request during register
        """
        username = attrs.get('username', '')  # Removing spaces from username

        # Username can only have number or alphabets
        if not username.isalnum():
            raise serializers.ValidationError({
                'username': 'Username should be of alphabetical characters and numbers only'
            })

        # Username should cannot start with numbers
        elif username[0].isdigit():
            raise serializers.ValidationError({
                'username': 'The username should start with alphabetical Characters'
            })

        return attrs

        def create(self, validated_data):
            """
            Writing Custom Code to create User Instance
            """
            user = models.CustomUser.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
            )

            return user
