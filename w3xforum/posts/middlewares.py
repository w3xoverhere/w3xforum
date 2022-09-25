from .models import Category


def categories_middleware(request):
    return {"categories": Category.objects.all()[:5]}