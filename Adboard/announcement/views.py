import json

from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import generics, permissions
from django.core.serializers.json import DjangoJSONEncoder

from .models import Post
from .serializer import BoardSerializer, BoardPageSerializer


class BoardListView(generics.ListAPIView):
    serializer_class = BoardSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "announcement/board_title.html"

    def get(self, request):
        queryset = Post.objects.all()
        return Response({'board_list': queryset})


class BoardPageListView(generics.ListAPIView):
    serializer_class = BoardPageSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "announcement/board_page.html"

    def get_queryset(self):
        queryset = Post.objects.filter(id=self.kwargs['pk'])
        return queryset

    def get(self, request, pk):
        queryset = self.get_queryset()
        return Response({'board_page': queryset})

