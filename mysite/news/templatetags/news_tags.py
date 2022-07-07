from django import template
from news.models import New, Category

register = template.Library()

@register.simple_tag(name='get_cats')
def get_cats_to_nav(filter=None):
    if not filter:
        return Category.objects.all()[:5]
    else:
        return Category.objects.filter(pk=filter)


@register.simple_tag(name='get_menu')
def get_menu_to_nav(active: str):
    menu = [
            {'name_link': 'Главная', 'name_path': 'index', 'params': None, 'status': 'default'},
            {'name_link': 'Новости', 'name_path': 'all_news', 'params': {'page': 1}, 'status': 'default'},   
            {'name_link': 'Предложить новость', 'name_path': 'add_new', 'params': None, 'status': 'default'},
    ]
    indexs = {
        'index': 0,
        'all_news': 1,
        'add_new': 2,
    }

    if active in indexs:
        menu[indexs[active]]['status'] = 'active'


    return menu


@register.inclusion_tag(filename='news/needful/cats.html', name='show_cats')
def show_block_cats(sort=None, cat_name=None):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {'cats': cats, 'cat_name': cat_name}


