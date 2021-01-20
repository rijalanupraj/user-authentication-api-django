# External Import
from rest_framework import generics, response, status

# Internal Import
from . import serializers
from . import models


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

            # Returning custom response while user is Created & Saved in Database
            return response.Response({
                'status': status.HTTP_201_CREATED,
                'message': 'Accont Created',
                'response': currentUserData
            })

