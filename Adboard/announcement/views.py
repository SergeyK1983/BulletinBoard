import re

from django.shortcuts import redirect
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from django_filters.rest_framework import DjangoFilterBackend

from cabinet.models import User
from .filters import BoardListFilter
from .forms import FormPost
from .models import Post
from .pagination import BoardListPagination
from .serializer import BoardSerializer, BoardPageSerializer
from .services import correct_form_category_for_serializer


class BoardListView(generics.ListAPIView):
    """ Вывод карточек всех объявлений на странице """

    serializer_class = BoardSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Post.objects.filter().all().order_by('-date_create')
    pagination_class = BoardListPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = BoardListFilter
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = "announcement/board_title.html"

    def get(self, request, *args, **kwargs):
        # все танцы с фильтрацией из-за пагинации в основном для TemplateHTMLRenderer, а так могло бы работать штатно.
        queryset = self.get_queryset()
        filter_board = self.filterset_class(self.request.GET, queryset)
        qs = filter_board.qs
        self.pagination_class.len_filter_qs = len(qs)  # для подсчета числа страничек, по другому будет глючить
        pages = self.paginate_queryset(queryset=qs)

        if request.headers.get('Content-Type') == 'application/json':
            if pages is not None:
                serializer = self.get_serializer(pages, many=True)
                return self.get_paginated_response(serializer.data)
            return self.list(request, *args, **kwargs)

        if pages is not None:
            return self.get_paginated_response(pages)
        return Response({"board_list": qs, "pagination": False})


class BoardPageListView(generics.ListAPIView):
    """ Вывод страницы с объявлением """

    serializer_class = BoardSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = "announcement/board_page.html"

    def get_queryset(self):
        queryset = Post.objects.filter(pk=self.kwargs['id'])
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not list(queryset):
            data = {'error': 'Такой страницы нет либо записей нет.', 'status': 'HTTP_404_NOT_FOUND'}
            if request.headers.get('Content-Type') == 'application/json':
                return Response(data, status=status.HTTP_404_NOT_FOUND)
            return Response({'error': data}, template_name='announcement/page_error.html')

        if request.headers.get('Content-Type') == 'application/json':
            return self.list(request, *args, **kwargs)
        return Response({'board_page': queryset})


class PageCreateView(generics.ListCreateAPIView):
    """ Создание нового объявления """

    serializer_class = BoardPageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # без этого с формы ничего не получить
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = "announcement/create_page.html"

    def get(self, request, *args, **kwargs):
        # метод get из-за TemplateHTMLRenderer
        if request.headers.get('Content-Type') == 'application/json':
            return Response(data={"Detail": "Метод GET не разрешен"}, status=status.HTTP_200_OK)

        user = User.objects.filter(username=request.user.username)
        form = FormPost()
        return Response({"profile": user, "form": form})  # "serializer": self.get_serializer() трудно настроить стили

    def post(self, request, *args, **kwargs):
        data = correct_form_category_for_serializer(request=request)
        serializer = BoardPageSerializer(data=data, context={'request': request})
        header = re.compile(r"^multipart/form-data")

        if not serializer.is_valid():
            data_err = {'error': serializer.errors, 'status': 'HTTP_400_BAD_REQUEST'}
            if header.search(request.headers.get('Content-Type')) and data.get('mark') is None:
                return Response(data_err, status=status.HTTP_400_BAD_REQUEST)
            return Response(data={'error': data_err}, template_name='announcement/page_error.html')

        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
            except ValidationError as e:  # лимит на публикации
                data_err = {'error': e.detail, 'status': 'HTTP_400_BAD_REQUEST'}
                if header.search(request.headers.get('Content-Type')) and data.get('mark') is None:
                    return Response(data_err, status=status.HTTP_400_BAD_REQUEST)
                return Response({'error': data_err}, template_name='announcement/page_error.html')
            except APIException:
                data_err = {'error': 'Сервер не отвечает.', 'status': 'HTTP_500_INTERNAL_SERVER_ERROR'}
                if header.search(request.headers.get('Content-Type')) and data.get('mark') is None:
                    return Response(data_err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response({'error': data_err}, template_name='announcement/page_error.html')

            if header.search(request.headers.get('Content-Type')) and data.get('mark') is None:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return redirect('board_list')


class PageUpdateView(generics.RetrieveUpdateAPIView):
    """ Контроллер изменения объявления """

    serializer_class = BoardPageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = "announcement/update_page_form.html"

    def get_queryset(self):
        queryset = Post.objects.filter(id=self.kwargs['id'])
        return queryset

    def get_object(self):
        obj = Post.objects.get(id=self.kwargs['id'])
        return obj

    def get(self, request, *args, **kwargs):
        if Post.objects.filter(id=self.kwargs['id']).exists():
            if Post.objects.get(id=self.kwargs['id']).author == request.user:
                if request.headers.get('Content-Type') == 'application/json':
                    return self.retrieve(request, *args, **kwargs)

                user = User.objects.filter(username=request.user.username)
                queryset = self.get_queryset()
                initial = {
                    "category": queryset[0].category,
                    "title": queryset[0].title,
                    "article": queryset[0].article,
                }
                form = FormPost(initial=initial)  # instance=queryset[0] все поля или initial переопределить поля
                return Response({"profile": user, "posts": queryset, "form": form})

        if request.headers.get('Content-Type') == 'application/json':
            return Response(data={"error": "Тут ничего нет!"}, status=status.HTTP_204_NO_CONTENT)
        return redirect("board_list")

    def post(self, request, *args, **kwargs):
        data = correct_form_category_for_serializer(request=request)
        instance = get_object_or_404(Post, id=kwargs['id'])  # можно еще так self.get_object()
        serializer = BoardPageSerializer(instance=instance, data=data, context={'request': request})
        header = re.compile(r"^multipart/form-data")

        if instance.author != request.user:
            if header.search(request.headers.get('Content-Type')) and data.get('mark') is None:
                return Response(data={"error": "Тут ничего нет!"}, status=status.HTTP_204_NO_CONTENT)
            return redirect("board_list")

        if not serializer.is_valid():
            data_err = {'error': serializer.errors, 'status': 'HTTP_400_BAD_REQUEST'}
            if header.search(request.headers.get('Content-Type')) and data.get('mark') is None:
                return Response(data_err, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': data_err}, template_name='announcement/page_error.html')

        if serializer.is_valid():
            try:
                # Если в .save() добавить owner=other/dict/, то добавит в validated_data и можно будет пользовать
                serializer.save()
            except APIException:
                data_err = {'error': 'Сервер не отвечает.', 'status': 'HTTP_500_INTERNAL_SERVER_ERROR'}
                if header.search(request.headers.get('Content-Type')) and data.get('mark') is None:
                    return Response(data_err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response({'error': data_err}, template_name='announcement/page_error.html')

            if header.search(request.headers.get('Content-Type')) and data.get('mark') is None:
                data_ = {'state': 1, 'message': 'Изменение прошло успешно'}
                return Response(data_, status=status.HTTP_200_OK)
            return redirect('board_list')


class PageDestroyView(generics.DestroyAPIView):
    """ Удаление объявления """

    serializer_class = BoardPageSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = "announcement/destroy_page.html"
    queryset = Post.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.queryset, id=self.kwargs['id'])
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            if request.headers.get('Content-Type') == 'application/json':
                return Response(data={'error': 'так нельзя делать!'}, status=status.HTTP_200_OK)
            return redirect('profile', request.user.id)

        self.perform_destroy(instance)
        if request.headers.get('Content-Type') == 'application/json':
            return Response(data={'status': 'Публикация удалена!'}, status=status.HTTP_204_NO_CONTENT)
        return redirect('profile', request.user.id)

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(username=request.user.username)
        data = {'profile': user}
        if request.headers.get('Content-Type') == 'application/json':
            return Response(data={'msg': 'Удаление публикаций', 'method': 'POST'}, status=status.HTTP_200_OK)
        return Response(data=data)

    def post(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

