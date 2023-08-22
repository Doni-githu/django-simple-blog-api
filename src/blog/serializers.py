from rest_framework import serializers
from .models import Blog
from src.users.serializers import UserSerializer
from src.base.services import delete_old_file
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['user', 'title', 'body', 'id', 'cover']
        model = Blog
        
    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)
    
class AuthorBlogSerializer(BlogSerializer):
    user = UserSerializer(read_only=True)