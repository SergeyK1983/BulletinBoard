from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from cabinet.models import User
from announcement.models import Post, Category
from ..models import CommentaryToAuthor


class TestAnnouncement(APITestCase):
    def setUp(self):
        self.author_post = User.objects.create(username="Sergey", email="exam1@gmail.com", password="wqxz9012")
        self.author_comment = User.objects.create(username="Dima", email="exam2@gmail.com", password="wqxz9012")

        self.category_TK = Category.objects.create(categories=Category.Categories.TANK)
        self.post_one = Post.objects.create(author=self.author_post, category=self.category_TK, title="Заголовок",
                                            article="article")

        self.comment = CommentaryToAuthor.objects.create(author=self.author_comment, to_post=self.post_one,
                                                         comment="Новый комментарий")

        self.c_post = APIClient()
        self.c_post.login(username='Sergey', password='wqxz9012', email="exam1@gmail.com")
        token = Token.objects.create(user=self.author_post)
        token.save()
        self.c_post.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.c_comment = APIClient()
        self.c_comment.login(username='Dima', password='wqxz9012', email="exam2@gmail.com")
        token = Token.objects.create(user=self.author_comment)
        token.save()
        self.c_comment.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_CommentCreateView_get(self):
        """ Создание комментария метод GET (не разрешен) """

        url = reverse(viewname='add-comment', kwargs={'id': self.post_one.id})
        response = self.c_comment.get(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'Detail': 'Метод GET не разрешен'})

    def test_CommentCreateView_post(self):
        """ Проверка создания комментария. Метод POST """

        url = reverse(viewname='add-comment', kwargs={'id': self.post_one.id})
        data = {
            "comment": "Отличная публикация!"
        }
        response = self.c_comment.post(url, data, format='json')
        instance = CommentaryToAuthor.objects.all().last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(instance.accepted)

    def test_UserCommentList(self):
        """ Просмотр собственных комментариев """

        url = reverse(viewname='my-comment', kwargs={'username': self.author_comment.username})
        response = self.c_comment.get(url, content_type='application/json')
        js = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(js[0]["accepted"], False)

    def test_PostCommentList(self):
        """ Просмотр комментариев на свои объявления """

        url = reverse(viewname='comments-to-post',
                      kwargs={'username': self.author_post.username, 'id': self.post_one.id})

        response = self.c_post.get(url, content_type='application/json')
        js = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(js[0]["accepted"], False)

    def test_CommentAcceptedUpdate(self):
        """ Принять комментарий """

        url = reverse(viewname='to-accepted', kwargs={'id': self.comment.id})
        data = {"accepted": "True"}
        response = self.c_post.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
