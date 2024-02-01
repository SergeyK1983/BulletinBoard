from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.exceptions import APIException
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.views import APIView

from .models import Post
from .serializer import BoardSerializer, BoardPageSerializer


class BoardListView(generics.ListAPIView):
    """ Вывод карточек всех объявлений на странице """

    serializer_class = BoardSerializer
    permission_classes = [permissions.AllowAny]
    # queryset = Post.objects.all().order_by('-date_create')
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "announcement/board_title.html"

    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all().order_by('-date_create')
        # return self.list(request, *args, **kwargs)
        return Response({'board_list': queryset})


class BoardPageListView(generics.ListAPIView):
    """ Вывод страницы с объявлением """

    serializer_class = BoardSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "announcement/board_page.html"

    def get_queryset(self):
        queryset = Post.objects.filter(id=self.kwargs['pk'])  # может вернуть пустой queryset
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not list(queryset):
            data = {'error': 'Такой страницы нет либо записей нет.',
                    'status': 'HTTP_404_NOT_FOUND'}
            # return Response(data, status=status.HTTP_404_NOT_FOUND)
            return HttpResponse(content=data.values(), status=status.HTTP_404_NOT_FOUND)

        # return self.list(request, *args, **kwargs)
        return Response({'board_page': queryset})


class PageCreateView(generics.CreateAPIView):  # generics.CreateAPIView
    """ Создание нового объявления """

    serializer_class = BoardPageSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "announcement/create_page.html"

    def get(self, request, *args, **kwargs):
        # метод только из-за TemplateHTMLRenderer
        return Response({"serializer": self.get_serializer()})

    def post(self, request, *args, **kwargs):
        # Контекст нужно передать, т.к. в сериалайзере используется поле с контекстом из request
        serializer = BoardPageSerializer(data=request.data, context={'request': request})
        print(request.data)

        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
                # return Response(serializer.data, status=status.HTTP_201_CREATED)
                return redirect('board_list')
            except APIException:
                data = {'error': 'Сервер не отвечает.', 'status': 'HTTP_500_INTERNAL_SERVER_ERROR'}
                return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class PageUpdateView(generics.UpdateAPIView):  # RetrieveUpdateAPIView
class PageUpdateView(generics.RetrieveUpdateAPIView):
    """ Контроллер изменения объявления """

    serializer_class = BoardPageSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "announcement/update_page.html"

    def get_queryset(self):
        queryset = Post.objects.filter(id=self.kwargs['pk'])
        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()  # экземпляр - не queryset, get_object_or_404(Post, pk=kwargs['pk'])
        serializer = BoardPageSerializer(instance=instance, data=request.data, context={'request': request})  # self.get_serializer

        if serializer.is_valid():
            try:
                # Если в .save() добавить owner=other/dict/, то добавит в validated_data и можно будет пользовать
                serializer.save()
                # data = {'state': 1, 'message': 'Изменение прошло успешно'}
                # return Response(data, status=status.HTTP_200_OK)
                return redirect('board_list')
            except APIException:
                data = {'error': 'Сервер не отвечает.', 'status': 'HTTP_500_INTERNAL_SERVER_ERROR'}
                return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PageDestroyView(generics.DestroyAPIView):
    """ Удаление объявления """

    serializer_class = BoardPageSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()

