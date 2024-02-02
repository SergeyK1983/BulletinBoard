from django.urls import path

from cabinet.views import ProfileDetail, ProfileArticleDetail, LoginUser, LogoutUser, RegisterUser, UpdateUser

urlpatterns = [
    path('v1/profile/<int:id>/', ProfileDetail.as_view(), name='profile'),
    path('v1/profile/<str:username>/<int:id>/', ProfileArticleDetail.as_view(), name='profile-article'),
    path('v1/profile/login/', LoginUser.as_view(), name='login'),
    path('v1/profile/login/<str:token>/', LoginUser.as_view(), name='login_confirm'),
    path('v1/profile/logout/', LogoutUser.as_view(), name='logout'),
    path('v1/profile/register/', RegisterUser.as_view(), name='register'),
    path('v1/profile/update/<int:id>/', UpdateUser.as_view(), name='update'),
]
