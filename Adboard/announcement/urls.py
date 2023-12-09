from django.urls import path

from announcement.views import BoardListView

urlpatterns = [
    path('v1/adboard/', BoardListView.as_view(), name="board_list"),
]
