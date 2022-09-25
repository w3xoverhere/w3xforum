from django.contrib import admin
from .models import Post, Category, Image


class ImageInline(admin.StackedInline):
    model = Image
    extra = 1


class PostAdmin(admin.ModelAdmin):
    list_display = ("trim50_title", "trim50_content", "category", "author", "is_published", "published")
    list_display_links = ("trim50_title", "trim50_content")
    list_filter = ("is_published", "published")
    inlines = [ImageInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)


