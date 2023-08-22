from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.response import Response
from .models import Blog
from .serializers import BlogSerializer, AuthorBlogSerializer
from src.base.services import delete_old_file
from rest_framework.mixins import status
class BlogView(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = AuthorBlogSerializer

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()
    
    def get_queryset(self):
        return super().get_queryset()
    
    def create(self, request, *args, **kwargs):
        serializer = BlogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)