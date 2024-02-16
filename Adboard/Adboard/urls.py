from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views

from Adboard.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('ann/', include('announcement.urls')),
    path('cab/', include('cabinet.urls')),
    path('com/', include('coment.urls')),
    path('auth/', views.obtain_auth_token, name='auth'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
