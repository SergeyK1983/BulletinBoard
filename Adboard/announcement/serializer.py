from rest_framework import serializers

from announcement.models import Post, Category


class CategorySerializer(serializers.ModelSerializer):
    """ Категории публикаций """
    class Meta:
        model = Category
        fields = ('categories', )
        extra_kwargs = {
            'categories': {'choices': Category.Categories.labels, },
        }


class BoardSerializer(serializers.ModelSerializer):
    """
    Вывод объявлений (списка, страницы)
    """
    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'category',
            'title',
            'article',
            'images',
            'files',
            'date_create'
        )


class BoardPageSerializer(serializers.ModelSerializer):
    """
    Создание, редактирование и удаление объявлений
    """
    # в поле автора подставляет текущего зарегистрированного пользователя, поле автора в запросе не отображает
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = (
            'author',
            'category',
            'title',
            'article',
            'images',
            'files',
        )

    @staticmethod
    def get_value_category(label):
        """ Выдает переменную из Categories модели Category по приходящему label """
        enum_category = Category.Categories
        list_category = list(enum_category)
        value = ""
        for i in range(len(list_category)):
            if label == list_category[i].label:
                value = list_category[i].value
                break
        else:
            if value == "":
                raise "Нет категории"  # TODO нужно доработать
        return value

    def create(self, validated_data):
        category = validated_data['category'].pop('categories')

        value = BoardPageSerializer.get_value_category(label=category)
        instance_category = Category.objects.get(categories=value)
        # TODO: except ObjectDoesNotExist:

        validated_data.update({'category': instance_category})
        instance = Post.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        category = validated_data['category'].pop('categories')

        value = BoardPageSerializer.get_value_category(label=category)
        instance_category = Category.objects.get(categories=value)

        validated_data.update({'category': instance_category})

        instance.category = validated_data.get('category', instance.category)
        instance.title = validated_data.get('title', instance.title)
        instance.article = validated_data.get('article', instance.article)
        instance.images = validated_data.get('images', instance.images)
        instance.files = validated_data.get('files', instance.files)

        instance.save()
        return instance
