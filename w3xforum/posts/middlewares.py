from django.db.models import Count

from .models import Category


def categories_middleware(request):
    cat = Category.objects.filter(post__gte=1)[:5]
    return {"categories": cat}