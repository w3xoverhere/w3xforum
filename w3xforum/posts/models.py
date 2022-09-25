from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("posts:category_detail", kwargs={"category_slug": self.slug})

def get_img_path(instance, filename):
    return "posts/%s" % (filename)


class Post(models.Model):
    title = models.CharField(max_length=90, verbose_name="Название", db_index=True, unique=True)
    content = models.TextField(db_index=True, verbose_name="Описание")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    author = models.ForeignKey(get_user_model(), blank=True, on_delete=models.CASCADE, verbose_name="Автор")
    is_published = models.BooleanField(default=False, verbose_name="Пост опубликован")
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Дата публикации")
    edited = models.DateTimeField(auto_now=True, verbose_name="Дата редактирования")

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-published", 'category', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:post_detail", kwargs={
            "category_slug": self.category.slug,
            "post_pk": self.pk,
        })

    def trim50_title(self):
        return u"%s..." % (self.title[:50],)

    def trim50_content(self):
        return u"%s..." % (self.content[:50],)


class Image(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    imgs = models.ImageField(upload_to=get_img_path, blank=True, verbose_name="Изображения")

