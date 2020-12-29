from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from .models import YTVideo
from .serializers import YTVideoSerializer
from rest_framework import filters

class ResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class YTVideosListAPIView(generics.ListAPIView):
    queryset = YTVideo.objects.all()
    serializer_class = YTVideoSerializer
    pagination_class = ResultsSetPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['title', 'description','thumbnail_url','publish_time']
    search_fields = ['title']
