from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from .models import YTVideo
from .serializers import YTVideoSerializer


class ResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class YTVideosListAPIView(generics.ListAPIView):
    queryset = YTVideo.objects.order_by('-publish_time').all()
    serializer_class = YTVideoSerializer
    pagination_class = ResultsSetPagination
