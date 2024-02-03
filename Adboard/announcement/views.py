from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import generics, permissions, status

from cabinet.models import User
from .forms import FormPost
from .models import Post, Category
from .serializer import BoardSerializer, BoardPageSerializer


class BoardListView(generics.ListAPIView):
    """ Вывод карточек всех объявлений на странице """

    serializer_class = BoardSerializer
    permission_classes = [permissions.AllowAny]
    # queryset = Post.objects.all().order_by('-date_create')  # в случае без TemplateHTMLRenderer
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
    parser_classes = (MultiPartParser, FormParser)  # без этого с формы ничего не получить
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "announcement/create_page.html"

    def get(self, request, *args, **kwargs):
        # метод get только из-за TemplateHTMLRenderer
        user = User.objects.filter(username=request.user.username)
        return Response({"profile": user, "serializer": self.get_serializer()})

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


class PageUpdateView(generics.RetrieveUpdateAPIView):
    """ Контроллер изменения объявления """

    serializer_class = BoardPageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "announcement/update_page_form.html"

    def get_queryset(self):
        queryset = Post.objects.filter(id=self.kwargs['pk'])
        return queryset

    def get(self, request, *args, **kwargs):
        # метод get только из-за TemplateHTMLRenderer
        user = User.objects.filter(username=request.user.username)
        queryset = self.get_queryset()
        initial = {
            "category": queryset[0].category,
            "title": queryset[0].title,
            "article": queryset[0].article,
        }
        form = FormPost(initial=initial)  # instance=queryset[0] все поля или initial переопределить поля
        # форма от serializer как-то криво работала
        return Response({"profile": user, "posts": queryset, "form": form})

    def post(self, request, *args, **kwargs):
        # костыль для формы, необходимо сменить содержание от формы в request.data, чтобы serializer не ругался
        data = request.data.copy()
        value = data.pop("category")
        label = Category.Categories(value[0]).label
        data.update({"category.categories": label})
        # конец костыля

        instance = get_object_or_404(Post, pk=kwargs['pk'])  # экземпляр - не queryset, можно еще так self.get_object()
        serializer = BoardPageSerializer(instance=instance, data=data, context={'request': request})

        if not serializer.is_valid():
            data = {'error': 'Что-то пошло не так ...', 'status': 'HTTP_400_BAD_REQUEST'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

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

