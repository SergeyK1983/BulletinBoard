from django.shortcuts import redirect
from rest_framework import generics, status, permissions
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from announcement.models import Post
from cabinet.models import User
from .forms import CommentCreateForm
from .serializer import CommentSerializer, CommentListSerializer, CommentAcceptedSerializer
from .models import CommentaryToAuthor
from .services import return_response


class PostCommentList(generics.RetrieveUpdateAPIView):
    """ Просмотр комментариев к своему объявлению """

    serializer_class = CommentListSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = "cabinet/profile_commentary_to_my_post.html"

    def get_queryset(self):
        queryset = CommentaryToAuthor.objects.filter(to_post__id=self.kwargs['pk']).order_by("-date_create")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        user = generics.get_object_or_404(User, username=kwargs['username'])
        if request.user != user:
            data = {"error": "Тут нет вашей страницы", 'status': 'HTTP_204_NO_CONTENT'}
            return return_response(request=request, data=data, status=status.HTTP_204_NO_CONTENT,
                                   template='announcement/page_error.html')

        if not Post.objects.filter(pk=kwargs['pk']).exists():
            data = {"error": "Такой публикации нет ...", 'status': 'HTTP_204_NO_CONTENT'}
            return return_response(request=request, data=data, status=status.HTTP_204_NO_CONTENT,
                                   template='announcement/page_error.html')

        user_qs = User.objects.filter(username=self.request.user.username)
        serializer = self.serializer_class(queryset, many=True)

        if request.headers.get('Content-Type') == 'application/json':
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"profile": user_qs, "comments": queryset, "com_page": True})


class UserCommentList(generics.ListAPIView):
    """ Просмотр своих комментариев к объявлениям других авторов на своей странице """

    serializer_class = CommentListSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = "cabinet/profile_my_commentary.html"

    def get_queryset(self):
        queryset = CommentaryToAuthor.objects.filter(author=self.request.user.username)
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        user = generics.get_object_or_404(User, username=kwargs['username'])
        if request.user != user:
            data = {"error": "Тут нет вашей страницы", 'status': 'HTTP_204_NO_CONTENT'}
            return return_response(request=request, data=data, status=status.HTTP_204_NO_CONTENT,
                                   template='announcement/page_error.html')

        user_qs = User.objects.filter(username=self.request.user.username)

        if request.headers.get('Content-Type') == 'application/json':
            return self.list(request, *args, **kwargs)
        return Response({"profile": user_qs, "comments": queryset, "com_page": True})


class CommentCreateView(generics.CreateAPIView):
    """ Создание комментария к объявлению """

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = "comment/add_comment.html"

    def get(self, request, *args, **kwargs):
        data = {"Detail": "Метод GET не разрешен"}
        if request.headers.get('Content-Type') == 'application/json':
            return Response(data, status=status.HTTP_200_OK)

        if Post.objects.filter(pk=kwargs['pk']).exists():
            to_post = Post.objects.filter(pk=kwargs['pk'])
            user = User.objects.get(username=request.user.username)
            initial = {
                'author': user.username,
                'to_post': to_post[0].title,
            }
            form = CommentCreateForm(initial=initial, request=request)
            return Response({"profile": user, "form": form, "url_post": to_post[0].get_absolute_url()})

        return redirect("board_list")

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request, 'kwargs': kwargs},
                                           partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        if request.headers.get('Content-Type') == 'application/json':
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return redirect('board_page', kwargs['pk'])


class CommentAcceptedUpdateView(generics.UpdateAPIView):
    """  Изменение статуса комментария на принято (accepted). """

    serializer_class = CommentAcceptedSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = "cabinet/profile_commentary_to_my_post.html"

    def get_queryset(self):
        queryset = CommentaryToAuthor.objects.filter(id=self.kwargs['pk'])
        return queryset

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not list(queryset):
            data = {"error": "Такого комментария нет ...", 'status': 'HTTP_204_NO_CONTENT'}
            return return_response(request=request, data=data, status=status.HTTP_204_NO_CONTENT,
                                   template='announcement/page_error.html')

        instance = queryset[0]

        serializer = self.serializer_class(instance, request.data)
        if not serializer.is_valid():
            data = {"error": serializer.errors, 'status': 'HTTP_400_BAD_REQUEST'}
            return return_response(request=request, data=data, status=status.HTTP_400_BAD_REQUEST,
                                   template='announcement/page_error.html')

        serializer.save()

        if request.headers.get('Content-Type') == 'application/json':
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return redirect('comments-to-post', request.user.username, instance.to_post.id)
