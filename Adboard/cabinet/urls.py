from django.urls import path

from .views import ProfileDetail, ProfileArticleDetail, LoginUser, LogoutUser, UpdateUserView, RegisterUser, \
    DestroyUserView, UserPasswordChange

urlpatterns = [
    path('v1/profile/<int:id>/', ProfileDetail.as_view(), name='profile'),
    path('v1/profile/<str:username>/<int:id>/', ProfileArticleDetail.as_view(), name='profile-article'),
    path('v1/profile/login/', LoginUser.as_view(), name='login'),
    path('v1/profile/logout/', LogoutUser.as_view(), name='logout'),
    path('v1/profile/register/', RegisterUser.as_view(), name='register'),
    path('v1/profile/destroy/', DestroyUserView.as_view(), name='destroy'),
    path('v1/profile/update/', UpdateUserView.as_view(), name='user-update'),
    path('v1/profile/change-pass/', UserPasswordChange.as_view(), name='change-pass'),
]
