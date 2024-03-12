from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from ..models import Post, Category
from cabinet.models import User


class TestAnnouncement(APITestCase):

    def setUp(self):
        self.category_TK = Category.objects.create(categories=Category.Categories.TANK)
        self.category_FR = Category.objects.create(categories=Category.Categories.FARRIER)
        self.author = User.objects.create_user(username="Serg", email="exam@gmail.com", password="wqxz9012")
        self.ann_page = Post.objects.create(author=self.author, category=self.category_TK, title="title",
                                            article="article")
        self.client = APIClient()
        self.client.login(username='Serg', password='wqxz9012', email="exam@gmail.com")
        token = Token.objects.create(user=self.author)
        token.save()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_BoardListView(self):
        """ Просмотр всех объявлений """

        url = reverse(viewname='board_list')
        response = self.client.get(url, content_type='application/json')
        js = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Ожидался код 200, а получил {response.status_code}.')
        self.assertEqual(response.accepted_media_type, 'application/json')
        self.assertIn('board_list', js)
        self.assertEqual(js['board_list'][0]['title'], 'title')

    def test_BoardPageListView(self):
        """ Просмотр одного объявления """

        url = reverse(viewname='board_page', kwargs={'id': self.ann_page.id})
        response = self.client.get(url, content_type='application/json')
        js = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(js[0]['author'], 'Serg')

    def test_BoardPageList_fail(self):
        """ Просмотр несуществующего объявлений """

        url = reverse(viewname='board_page', kwargs={'id': 100})
        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {
            "error": "Такой страницы нет либо записей нет.",
            "status": "HTTP_404_NOT_FOUND"
        })

    def test_PageCreateView(self):
        """ Создание объявления """

        data = {'category': 'FR', 'title': 'Кузнец', 'article': 'New post'}
        response = self.client.post(reverse('board-page-create'), data, format='multipart')
        instanse = Post.objects.all().last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.all().count(), 2)
        self.assertEqual(instanse.category.categories, "FR")

    def test_PageCreateView_fail(self):
        """ Создание объявления с ошибкой """

        data = {'category': 'FR1', 'title': 'Кузнец', 'article': 'New post'}
        response = self.client.post(reverse('board-page-create'), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

