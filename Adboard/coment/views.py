from django.shortcuts import redirect
from rest_framework import generics, status, permissions
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from announcement.models import Post
from cabinet.models import User
from .forms import CommentCreateForm
from .serializer import CommentSerializer


class CommentList(generics.ListAPIView):
    """ Просмотр своих комментариев к объявлениям на своей странице """

    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]


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

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        if request.headers.get('Content-Type') == 'application/json':
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return redirect('board_page', kwargs['pk'])


