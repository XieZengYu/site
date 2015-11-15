from django.conf.urls import include, url
from django.contrib import admin

from .views import *


urlpatterns = [
    url(r'^login/', Login.as_view()),
]
