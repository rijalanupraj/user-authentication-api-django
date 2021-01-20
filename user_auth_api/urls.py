# External Import
from django.contrib import admin
from django.urls import path, include

# Internal Import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('user.urls')),
]
