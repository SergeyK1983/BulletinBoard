from django.urls import path
from .views import CommentCreateView, UserCommentList

urlpatterns = [
    path('v1/add-comment/<int:pk>/', CommentCreateView.as_view(), name='add-comment'),
    path('v1/<str:username>/my-comment/', UserCommentList.as_view(), name='my-comment'),
]
