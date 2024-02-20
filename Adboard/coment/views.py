from django.shortcuts import redirect
from rest_framework import generics, status, permissions
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from announcement.models import Post
from cabinet.models import User
from .forms import CommentCreateForm
from .serializer import CommentSerializer


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = "comment/add_comment.html"

    def get(self, request, *args, **kwargs):
        to_post = Post.objects.filter(pk=kwargs['pk'])
        user = User.objects.get(username=request.user.username)
        initial = {
            'author': user.username,
            'to_post': to_post[0].title,
        }
        form = CommentCreateForm(initial=initial, request=request)
        data = {"Detail": "Метод GET не разрешен"}
        if request.headers.get('Content-Type') == 'application/json':
            return Response(data, status=status.HTTP_200_OK)
        return Response({"profile": user, "form": form})

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request, 'kwargs': kwargs}, partial=True)

        if serializer.is_valid(raise_exception=True):
            print("пытаюсь сохранить")
            serializer.save()
            print("сохранено")

        return redirect('board_page', kwargs['pk'])


