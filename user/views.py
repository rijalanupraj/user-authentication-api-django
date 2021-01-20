# External Import
from rest_framework import generics

# Internal Import
from . import serializers

class UserRegistrationView(generics.GenericAPIView):
    """
    A Generic API View to register new User
    """

    serializer_class = serializers.UserRegistrationSerializer

    def post(self,request):
        """
        Post Request for User Registration
        """
