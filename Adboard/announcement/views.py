from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import generics, permissions

from .models import Post
from .serializer import BoardSerializer


class BoardListView(generics.ListAPIView):
    serializer_class = BoardSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "announcement/board_title.html"

    def get(self, request):
        queryset = Post.objects.all()
        return Response({'board_list': queryset})
