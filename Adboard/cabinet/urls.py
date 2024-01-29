from django.urls import path

from cabinet.views import ProfileDetail, ProfileArticleDetail, LoginUser, LogoutUser, RegisterUser, UpdateUser

urlpatterns = [
    path('profile/<int:id>/', ProfileDetail.as_view(), name='profile'),
    path('profile/<str:username>/<int:id>/', ProfileArticleDetail.as_view(), name='profile-article'),
    path('profile/login/', LoginUser.as_view(), name='login'),
    path('profile/login/<str:token>/', LoginUser.as_view(), name='login_confirm'),
    path('profile/logout/', LogoutUser.as_view(), name='logout'),
    path('profile/register/', RegisterUser.as_view(), name='register'),
    path('profile/update/<int:id>/', UpdateUser.as_view(), name='update'),
]
