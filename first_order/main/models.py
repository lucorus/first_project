from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class CustomUser(AbstractUser):
    status = models.CharField(max_length=30, blank=True, verbose_name="Статус")
    avatar = models.ImageField(upload_to='photos', blank=True, verbose_name="Аватар")
    level = IntegerRangeField(max_value=3, min_value=1, default=1, verbose_name="Уровень доступа")
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.slug})

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class History(models.Model):
    title = models.CharField(max_length=35, unique=True, verbose_name="Название")
    text = models.TextField(verbose_name="Текст")
    level = IntegerRangeField(max_value=3, min_value=1, default=1, verbose_name="Уровень доступа")
    created_add = models.DateTimeField(auto_now_add=True, verbose_name='Создано в')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Автор')
    image = models.ImageField(upload_to='Album', blank=True, verbose_name='Изображение')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'История'
        verbose_name_plural = 'Истории'


class Category(models.Model):
    title = models.CharField(max_length=25, verbose_name="Название", unique=True)
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse('', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title
