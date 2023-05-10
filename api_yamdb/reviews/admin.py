from django.contrib import admin

from .models import Review, Title, User, Comment, Genre, Category, TitleGenre


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author', 'score', 'text')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'author', 'text')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')


class TGAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre')


admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(User)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(TitleGenre, TGAdmin)
