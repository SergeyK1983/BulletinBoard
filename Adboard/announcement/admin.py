from django.contrib import admin
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'category', 'title', 'images', 'files', 'date_create')
    list_display_links = ('author',)
    search_fields = ('author', 'category')
    list_filter = ('category', )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'categories')
    list_display_links = ('categories',)


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
