from django.urls import path

from announcement.views import BoardListView, BoardPageListView, PageCreateView, PageDestroyView, PageUpdateView

urlpatterns = [
    path('v1/adboard/', BoardListView.as_view(), name="board_list"),
    path('v1/adboard/page/create/', PageCreateView.as_view(), name="board-page-create"),
    path('v1/adboard/page/<int:id>/', BoardPageListView.as_view(), name="board_page"),
    path('v1/adboard/page/<int:id>/destroy/', PageDestroyView.as_view(), name="board_page-destroy"),
    path('v1/adboard/page/<int:id>/update/', PageUpdateView.as_view(), name="board_page-update"),
]
