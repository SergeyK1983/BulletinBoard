from django.urls import path
from .views import comment_create

urlpatterns = [
    path('comment/', comment_create, name='create_comment'),
]
