from django import template
from news.models import New, Category

register = template.Library()

@register.simple_tag(name='get_cats')
def get_cats_to_nav(filter=None):
    if not filter:
        return Category.objects.all()[:5]
    else:
        return Category.objects.filter(pk=filter)


@register.inclusion_tag(filename='news/needful/cats.html', name='show_cats')
def show_block_cats(sort=None, cat_name=None):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {'cats': cats, 'cat_name': cat_name}


