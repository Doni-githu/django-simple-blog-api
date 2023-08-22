from django.db import models
from src.users.models import User
from src.base.services import get_path_for_blog_cover, validate_size_image
from django.core.validators import *
class Blog(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    cover = models.ImageField(
        upload_to='blog/cover/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png']), validate_size_image]
    )
    
    def __str__(self):
        return self.title
    