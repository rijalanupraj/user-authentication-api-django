# External Import
from rest_framework import serializers
from django.contrib import auth


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
        model = models.User
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
            user = models.User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
            )

            return user


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer to Login User
    You can login in by using either email
    or password
    """
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)

    class Meta:
        model = models.User
        fields = ['email', 'username', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
        }

    def validate(self, attrs):
        """
        Validating the User loging credentials
        """
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        email = attrs.get('email', '')
        if username == "" and email == "":

            raise serializers.ValidationError(
                {"errors": "Both username and email cannot be null"})
        if username != "" and email != "":

            current_user = auth.authenticate(
                username=username, password=password)
        elif username != "":

            current_user = auth.authenticate(
                username=username, password=password)
        elif email != "":

            try:
                username = models.User.objects.get(email=email).username
            except:
                raise serializers.ValidationError('Invalid Credentials')
            current_user = auth.authenticate(
                username=username, password=password)

        if not current_user:
            raise serializers.ValidationError('Invalid Credentials')

        if not current_user.is_verified:
            raise serializers.ValidationError('Account Not Verified')

        return {
            'username': current_user.username,
            'email': current_user.email,
        }
