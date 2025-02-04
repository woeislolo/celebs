from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from unidecode import unidecode
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class Men(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(verbose_name='Статья')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Автор статьи')
    tags = TaggableManager()

    objects = models.Manager()
    published = PublishedManager()
                    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = unidecode(self.title.lower().replace(' ', '_'))
        super(Men, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Известные мужчины'
        verbose_name_plural = 'Известные мужчины'
        ordering = ['-time_create', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'
        ordering = ['id', ]


class Comment(models.Model):
    post = models.ForeignKey(Men, on_delete=models.CASCADE, related_name='comments', verbose_name='Статья')
    author = models.CharField(max_length=80, verbose_name='Автор')
    email = models.EmailField(verbose_name='Email')
    content = models.TextField(verbose_name='Комментарий')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    active = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return f'Комментарий пользователя {self.author} к статье {self.post}'
    
    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'
        ordering = ['time_create',]
        indexes = [
            models.Index(fields=['time_create',]),
        ]
