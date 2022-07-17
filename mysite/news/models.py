from django.db import models

from django.urls import reverse

from django.core.exceptions import ValidationError


# Модель новостей
class New(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, null=True, verbose_name="URL", error_messages={'unique': 'Ошибка в URL'})
    content = models.TextField(blank=True, verbose_name="Содержание")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    photo = models.ImageField(upload_to="%Y/%m/%d", verbose_name="Фото")
    is_published = models.BooleanField(default=True, verbose_name="Статус публикации")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория")

    def __str__(self):
        return f"{self.title} ({self.pk})"

    def get_absolute_url(self):
        return reverse('new', kwargs={'new_slug': self.slug})

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-id"]


# Модель категорий
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название категории")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, null=True, verbose_name="URL")

    def __str__(self):
        return f"{self.name} ({self.pk})"

    def get_absolute_url(self):
        return reverse('news_by_cat', kwargs={'cat_slug': self.slug})


    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["id"]