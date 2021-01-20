# External Import
from django.contrib import admin

# Internal Import
from user.models import CustomUser

admin.site.register(CustomUser)