from django.contrib import admin
from django.utils.safestring import mark_safe  # не экранирует теги, можно выполнить переданный код

from .models import *


class MenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_preview_photo', 'is_published')  # что доп. отображаем в админке
    list_display_links = ('id', 'title')  # кликабельные поля для перехода на пост
    search_fields = ('title', 'content')  # по каким полям возможен поиск
    list_editable = ('is_published',)  # дает возможность редактировать указ.поле
    list_filter = ('is_published', 'time_create')  # дает возможность фильтровать
    prepopulated_fields = {'slug': ('title',)}  # генерирует слаг на основе названия модели

    def get_preview_photo(self, object):  # object ссылается на текущий объект класса Men в моделях (это админка)
        return mark_safe(f"<img src='{object.photo.url}' width=60>")

    get_preview_photo.short_description = 'Превью фото'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)


admin.site.register(Men, MenAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Админ-панель сайта Celebs'
admin.site.site_header = 'Сайт Celebs'
