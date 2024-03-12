from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from announcement.models import Category, Post
from ..models import User


class TestCabinet(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="Sergey", email="exam1@gmail.com", password="wqxz9012")
        self.user_fake = User.objects.create(username="Dima", email="exam2@gmail.com", password="wqxz9012")

        self.category_TK = Category.objects.create(categories=Category.Categories.TANK)
        self.post_one = Post.objects.create(author=self.user, category=self.category_TK, title="Заголовок",
                                            article="Самая интересная публикация!")
        self.post_two = Post.objects.create(author=self.user, category=self.category_TK, title="Заглавие",
                                            article="Вторая интересная публикация!")

        self.c_user = APIClient()
        self.c_user.login(username='Sergey', password='wqxz9012', email="exam1@gmail.com")
        token = Token.objects.create(user=self.user)
        token.save()
        self.c_user.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.c_user_fake = APIClient()
        self.c_user_fake.login(username='Dima', password='wqxz9012', email="exam2@gmail.com")
        token = Token.objects.create(user=self.user_fake)
        token.save()
        self.c_user_fake.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_ProfileDetail(self):
        """ Страница пользователя """

        url = reverse(viewname='profile', kwargs={"id": self.user.id})
        response = self.c_user.get(url, content_type='application/json')
        js = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(js), 1)
        self.assertEqual(len(js[0]["posts"]), 2)
        self.assertEqual(js[0]["username"], self.user.username)

    def test_ProfileDetail_no_user(self):
        """ Страница пользователя, пользователя не существует """

        url = reverse(viewname='profile', kwargs={"id": 100})
        response = self.c_user.get(url, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_ProfileDetail_fake_user(self):
        """ Страница пользователя, ложный пользователь """

        url = reverse(viewname='profile', kwargs={"id": self.user_fake.id})
        response = self.c_user.get(url, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_ProfileDetail_not_auth(self):
        """ Страница пользователя, не авторизованный пользователь """

        url = reverse(viewname='profile', kwargs={"id": self.user.id})
        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ProfileArticleDetail(self):
        """ Публикация со страницы пользователя """

        url = reverse(viewname='profile-article', kwargs={"username": self.user.username, "id": self.post_one.id})
        response = self.c_user.get(url, content_type='application/json')
        js = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(js[0]["post"]), 1)
        self.assertIn('title', js[0]["post"][0])
        self.assertEqual(js[0]["username"], self.user.username)

    def test_ProfileArticleDetail_no_post(self):
        """ Публикация со страницы пользователя, публикации не существует """

        url = reverse(viewname='profile-article', kwargs={"username": self.user.username, "id": 100})
        response = self.c_user.get(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_ProfileArticleDetail_fake_user(self):
        """ Публикация со страницы пользователя, ложный пользователь """

        url = reverse(viewname='profile-article', kwargs={"username": self.user_fake.username, "id": self.post_one.id})
        response = self.c_user.get(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_ProfileArticleDetail_not_auth(self):
        """ Публикация со страницы пользователя, пользователь не авторизован """

        url = reverse(viewname='profile-article', kwargs={"username": self.user.username, "id": self.post_one.id})
        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
