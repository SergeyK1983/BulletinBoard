from django.urls import path

from cabinet.views import get_profile, ProfileDetail

urlpatterns = [
    path('', get_profile, name='prof'),
    path('<int:id>', ProfileDetail.as_view(), name='profile')
]
