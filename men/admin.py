from django.contrib import admin
from django.utils.safestring import mark_safe  # не экранирует теги, можно выполнить переданный код

from .models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_of_birth', 'get_preview_photo',)
    raw_id_fields = ('user',)

    def get_preview_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=60>")
        return None

    get_preview_photo.short_description = 'Превью фото'


@admin.register(Men)
class MenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_preview_photo', 'is_published', 'author', 'time_create', 'time_update')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content', 'author')
    list_editable = ('is_published',)  # дает возможность редактировать указ.поле
    list_filter = ('is_published', 'time_create')  # дает возможность фильтровать
    prepopulated_fields = {'slug': ('title',)}  # генерирует слаг на основе названия модели

    def get_preview_photo(self, object):
        return mark_safe(f"<img src='{object.photo.url}' width=60>")

    get_preview_photo.short_description = 'Превью фото'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'email', 'content', 'post', 'time_create', 'active')
    list_filter = ('active', 'time_create', 'time_update')
    search_fields = ('author', 'email', 'content')
    list_editable = ('active',)
    list_filter = ('author', 'active', 'time_create')


admin.site.site_title = 'Админ-панель сайта Celebs'
admin.site.site_header = 'Сайт Celebs'
