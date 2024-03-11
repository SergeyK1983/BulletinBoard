from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from ..models import Category
from ..services import correct_form_category_for_serializer


class RequestForTest:
    def __init__(self, request):
        self.request = request

    @property
    def data(self):
        return self.request


class TestCorrectFormCategoryForSerializer(APITestCase):

    def setUp(self):
        """ Исходные данные """

        self.request_in = RequestForTest(
            {'category': ['FR'], 'title': ['title'], 'article': ['article'], 'images': [''], 'files': [''],
             'mark': ['True']})
        self.request_in_fail = RequestForTest(
            {'category': ['FR1'], 'title': ['title'], 'article': ['article'], 'images': [''], 'files': [''],
             'mark': ['True']})
        self.category_FR = Category.Categories.FARRIER

    def test_correct_form_category_for_serializer(self):
        correct_level = Category.Categories.FARRIER.label
        data = correct_form_category_for_serializer(request=self.request_in)
        self.assertEqual(data['category.categories'], correct_level)

    def test_fail_correct_form_category_for_serializer(self):
        """ Ошибка неверного имени категории """
        with self.assertRaises(ValidationError):
            correct_form_category_for_serializer(request=self.request_in_fail)

