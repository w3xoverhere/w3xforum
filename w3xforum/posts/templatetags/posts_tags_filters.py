from django import template


register = template.Library()


@register.filter
def count_is_published(cat):
    return cat.post_set.filter(is_published=True).count()