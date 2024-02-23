from django.urls import path
from .views import CommentCreateView, UserCommentList, PostCommentList, CommentAcceptedUpdateView

urlpatterns = [
    path('v1/add-comment/<int:pk>/', CommentCreateView.as_view(), name='add-comment'),
    path('v1/<str:username>/my-comment/', UserCommentList.as_view(), name='my-comment'),
    path('v1/<str:username>/<int:pk>/comments-to-post/', PostCommentList.as_view(), name='comments-to-post'),
    path('v1/comments-to-accepted/<int:pk>/', CommentAcceptedUpdateView.as_view(), name='to-accepted'),
]
