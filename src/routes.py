from django.urls import path, include

urlpatterns = [
    path('users/', include('src.users.urls')),
    path('blog/', include('src.blog.urls'))
]