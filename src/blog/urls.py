from django.urls import path
from . import views

urlpatterns = [
    path("", views.BlogView.as_view({"get": "list", "post": "create"})),
    path(
        "<int:pk>/",
        views.BlogView.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
]
