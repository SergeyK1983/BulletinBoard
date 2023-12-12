from django.urls import path

from cabinet.views import ProfileDetail, ProfileList

urlpatterns = [
    path('profile/<int:id>/', ProfileDetail.as_view(), name='profile'),
    path('profile/<int:id>/list/', ProfileList.as_view(), name='profilelist'),
]
