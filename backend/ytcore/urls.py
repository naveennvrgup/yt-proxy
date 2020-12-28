from django.urls import path
from .views import YTVideosListAPIView

urlpatterns = [
    path('ytproxy/',YTVideosListAPIView.as_view()),
]