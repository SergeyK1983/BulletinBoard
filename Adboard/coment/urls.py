from django.urls import path
from .views import CommentCreateView

urlpatterns = [
    path('v1/add-comment/<int:pk>/', CommentCreateView.as_view(), name='add-comment'),
]
