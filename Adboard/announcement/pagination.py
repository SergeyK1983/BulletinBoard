from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Post


class BoardListPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 40

    def get_pages_count(self):
        """
        Добавлено. Определение количества получившихся страниц для пагинации.
        Заимствовано из rest_framework/pagination.py _divide_with_ceil(a, b)
        """
        count_posts = Post.objects.all().count()
        if count_posts % self.page_size:
            return (count_posts // self.page_size) + 1
        return count_posts // self.page_size

    def get_paginated_response(self, data):
        return Response({
            "links": {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'context': self.get_html_context if self.request.headers.get('Content-Type') == 'text/plain' else None,  # для пагинации при TemplateHTMLRenderer
            'count': self.page.paginator.count,
            'pages_count': self.get_pages_count(),
            'board_list': data,
            'pagination': True,
        })
