from django import template
from courses.models import Category, Favourite

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.simple_tag()
def get_favourite(user, article):
    if Favourite.objects.filter(user=user, article=article):
        return True
    else:
        return False