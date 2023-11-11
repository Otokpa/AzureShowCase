from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_transcript, name='get_transcript'),
]
