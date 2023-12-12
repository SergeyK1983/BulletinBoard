from django.urls import path

from announcement.views import BoardListView, BoardPageListView

urlpatterns = [
    path('v1/adboard/', BoardListView.as_view(), name="board_list"),
    path('v1/adboard/page/<int:pk>/', BoardPageListView.as_view(), name="board_page"),
]
