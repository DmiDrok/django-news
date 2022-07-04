from django.shortcuts import render
from django.http import HttpResponse

from .models import New, Category

# Обработчик главной страницы
def index(request):
    menu = [
        {'name_link': 'Главная', 'name_path': 'index', 'status': 'active'},
        {'name_link': 'Новости', 'name_path': 'all_news', 'status': 'default'}
    ]

    data = {
        'menu': menu
    }

    return render(request, 'news/index.html', context=data)


# Обработчик новостей 
def all_news(request):
    news = New.objects.all()
    menu = [
        {'name_link': 'Главная', 'name_path': 'index', 'status': 'default'},
        {'name_link': 'Новости', 'name_path': 'all_news', 'status': 'active'}
    ]

    data = {
        'news': news,
        'menu': menu,
    }

    return render(request, 'news/all_news.html', context=data)


# Обработчик одной новости
def new(request, new_id):
    new = New.objects.get(pk=new_id)
    menu = [
        {'name_link': 'Главная', 'name_path': 'index', 'status': 'default'},
        {'name_link': 'Новости', 'name_path': 'all_news', 'status': 'default'}
    ]

    data = {
        'new': new,
        'menu': menu,
    }

    return render(request, 'news/new.html', context=data)


# Обработчик новостей по категориям
def news_by_cat(request, cat_id):
    news = New.objects.filter(cat_id=cat_id)
    cat_name = Category.objects.get(pk=cat_id).name

    menu = [
        {'name_link': 'Главная', 'name_path': 'index', 'status': 'default'},
        {'name_link': 'Новости', 'name_path': 'all_news', 'status': 'default'}
    ]

    data = {
        'news': news,
        'menu': menu,
        'cat_name': cat_name,
    }

    return render(request, 'news/news_by_cat.html', context=data)