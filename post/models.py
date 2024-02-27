from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify


User = get_user_model()

class Category(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True, blank=True)
    title = models.CharField(max_length=100, verbose_name='Название', unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()

    


class Tag(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True, blank=True)
    title = models.CharField(max_length=100, verbose_name='Название', unique=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()


class Post(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True, blank=True)
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='posts_img/', blank=True, verbose_name='Картинка')
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name='posts', verbose_name='Автор')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()