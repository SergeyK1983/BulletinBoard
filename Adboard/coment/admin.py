from django.contrib import admin
from .models import CommentaryToAuthor


class CommentaryToAuthorAdmin(admin.ModelAdmin):
    list_display = ('author', 'to_post', 'comment', 'accepted', 'date_create')
    list_display_links = ('author', 'to_post')
    search_fields = ('author', )
    list_filter = ('accepted',)


admin.site.register(CommentaryToAuthor, CommentaryToAuthorAdmin)
