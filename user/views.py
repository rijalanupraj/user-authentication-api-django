# External Import
from rest_framework import generics, response, status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site

# Internal Import
from . import serializers
from . import models
from .utils import Util


class UserRegistrationView(generics.GenericAPIView):
    """
    A Generic API View to register new User
    """

    serializer_class = serializers.UserRegistrationSerializer

    def post(self, request):
        """
        Post Request for User Registration
        """
        currentUser = request.data  # Storing the POST data in a variable

        serializer = self.serializer_class(data=currentUser)

        # Working on the data if only the data provided of the user is valid
        # Serializer checks the validity of the USER Post Request Data
        if serializer.is_valid():
            serializer.save()  # Saving the data to database
            currentUserData = serializer.data

            user = models.User.objects.get(email=currentUserData['email'])

            # Token
            token = str(RefreshToken().for_user(user).access_token)

            # Sending Verification URL to the current_user
            current_site = get_current_site(request)
            relative_link = reverse('verify-email')
            absolute_url = f"http://{current_site}{relative_link}?token={token}"
            email_body = f"Namaste {user.username}\n Use link below to verify your account.\n{absolute_url}"
            email_message = {
                'email_body': email_body,
                'email_subject': "Verify Your Email For SlicedTv Account",
                'to_email': user.email
            }
            # Sending from utils.py file
            Util.send_email(email_message)

            # Returning custom response while user is Created & Saved in Database
            return response.Response({
                'status': status.HTTP_201_CREATED,
                'message': 'Accont Created',
                'response': currentUserData
            })
        else:
            message = 'Invalid'
            if "errors" in serializer._errors:
                message = serializer._errors['errors'][0]
            return response.Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': message,
                'response': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(generics.GenericAPIView):
    """
    A Generic API View to login
    """
    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return response.Response({
                'status': status.HTTP_200_OK,
                'message': 'Logged In Successful',
                'response': serializer.data,
            }, status=status.HTTP_200_OK)
        else:
            message = 'Invalid'
            if "errors" in serializer._errors:
                message = serializer._errors['errors'][0]
            return response.Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': message,
                'response': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
