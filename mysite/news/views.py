from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404


from .models import New, Category


import math


# Обработчик главной страницы
def index(request):
    menu = [
        {'name_link': 'Главная', 'name_path': 'index', 'params': None, 'status': 'active'},
        {'name_link': 'Новости', 'name_path': 'all_news', 'params': {'page': 1}, 'status': 'default'}
    ]

    data = {
        'menu': menu,
    }

    return render(request, 'news/index.html', context=data)


# Обработчик новостей 
def all_news(request, num_page):
    news = None # Список всех новостей
    if num_page == 0:
        return redirect('all_news', 1)
    else:
        now_page = num_page-1
        news = New.objects.filter(is_published=True)[now_page*3:now_page*3+3]
    
    all_news = New.objects.filter(is_published=True)
    paginate_pages = None # Тут будет количество всех страниц
    if len(all_news) > 3: # Если количество опубликованных новостей больше 3 - то делаем пагинацию
        paginate_pages = range(1, math.ceil((len(all_news) // 3 + 1))+1)
    

    menu = [
        {'name_link': 'Главная', 'name_path': 'index', 'params': None, 'status': 'default'},
        {'name_link': 'Новости', 'name_path': 'all_news', 'params': {'page': 1}, 'status': 'active'}
    ]
    
    data = {
        'news': news,
        'menu': menu,
        'paginate_pages': paginate_pages,
        'num_page': num_page,
    }

    return render(request, 'news/all_news.html', context=data)


# Обработчик одной новости
def new(request, new_slug):
    new = get_object_or_404(New, slug=new_slug, is_published=True)

    menu = [
        {'name_link': 'Главная', 'name_path': 'index', 'params': None, 'status': 'default'},
        {'name_link': 'Новости', 'name_path': 'all_news', 'params': {'page': 1}, 'status': 'active'}
    ]
    cats = Category.objects.all()[:5]

    data = {
        'new': new,
        'menu': menu,
        'cats': cats,
    }

    return render(request, 'news/new.html', context=data)


# Обработчик новостей по категориям
def news_by_cat(request, cat_slug):
    cat = get_object_or_404(Category, slug=cat_slug)
    news = New.objects.filter(cat_id=cat.id, is_published=True)
    cat_name = cat.name

    menu = [
        {'name_link': 'Главная', 'name_path': 'index', 'params': None, 'status': 'default'},
        {'name_link': 'Новости', 'name_path': 'all_news', 'params': {'page': 1}, 'status': 'active'}
    ]

    data = {
        'news': news,
        'menu': menu,
        'cat_name': cat_name,
    }

    return render(request, 'news/news_by_cat.html', context=data)

# Обработчик 'страница не найдена'
def pageNotFound(request, exception):
    menu = [
        {'name_link': 'Главная', 'name_path': 'index', 'params': None, 'status': 'default'},
        {'name_link': 'Новости', 'name_path': 'all_news', 'params': {'page': 1}, 'status': 'default'}
    ]

    data = {
        'menu': menu,
    }


    return render(request, 'news/404.html', context=data)