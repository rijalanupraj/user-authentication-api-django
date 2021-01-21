# External Import
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    """
    Custom User Manager for Custom User Profile
    """

    def create_user(self, username, email, password=None):
        """
        Create a new user profile
        """
        # The Username and Email cannot be Null
        if username is None:
            raise ValueError("User Must Have a Username")
        if email is None:
            raise ValueError("User Must Have an Email")

        # Removing unnecessary things from email(example:spaces)
        email = self.normalize_email(email)

        # Creating a user instance
        user = self.model(username=username, email=email)

        # Set Password Method automatically hashes the password and saves.
        # It increases Security
        user.set_password(password)

        # Save the current user instance to the database
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password=None):
        """
        Create superuser from using create_user function
        """
        if password is None:
            raise ValueError('Password should not be none')

        # Creating user instance and saving it to database
        user = self.create_user(username, email, password)

        # Assigning current user as superuser
        user.is_superuser = True
        user.is_staff = True

        # Saving the modified data to the database
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model for the Django Application.
    Needed to create this as we need email field.
    """

    username = models.CharField(max_length=90, unique=True)
    # I you want to create different account from same email, set the value to false.
    email = models.CharField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        """
        Returns User's id and username
        """
        return f"{self.id} | {self.username}"

    def tokens(self):
        """ Genreate Access and Refresh Token for current user """
        user_token = RefreshToken.for_user(self)
        return {
            'refresh': str(user_token),
            'access': str(user_token.access_token),
        }
