from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404

from .models import New, Category
from .forms import AddNewForm

import math


# Обработчик главной страницы
def index(request):
    active = 'index'
    data = {
        'active': active,
    }

    return render(request, 'news/index.html', context=data)


# Обработчик новостей 
def all_news(request, num_page):
    if num_page == 0:
        return redirect('all_news', 1)
    else:
        now_page = num_page - 1
        news = New.objects.filter(is_published=True)[now_page * 3:now_page * 3 + 3]

    all_news = New.objects.filter(is_published=True)
    paginate_pages = None  # Тут будет количество всех страниц
    if len(all_news) > 3:  # Если количество опубликованных новостей больше 3 - то делаем пагинацию
        paginate_pages = range(1, math.ceil((len(all_news) // 3 + 1)) + 1)

    active = 'all_news'
    data = {
        'news': news,
        'active': active,
        'paginate_pages': paginate_pages,
        'num_page': num_page,
    }

    return render(request, 'news/all_news.html', context=data)


# Обработчик одной новости
def new(request, new_slug):
    new = get_object_or_404(New, slug=new_slug, is_published=True)
    cats = Category.objects.all()[:5]
    active = 'all_news'

    data = {
        'new': new,
        'active': active,
        'cats': cats,
    }

    return render(request, 'news/new.html', context=data)


# Обработчик новостей по категориям
def news_by_cat(request, cat_slug):
    news = New.objects.filter(cat__slug=cat_slug, is_published=True)
    cat_name = news[0].cat.name

    active = 'all_news'

    data = {
        'news': news,
        'active': active,
        'cat_name': cat_name,
    }

    return render(request, 'news/news_by_cat.html', context=data)


# Обработчик добавления новости
def add_new(request):
    active = 'add_new'

    if request.method == 'POST':
        print(request.POST, "- Данные.")
        print(request.FILES, "- Файлы.")
        form = AddNewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AddNewForm()

    data = {
        'active': active,
        'form': form,
    }

    return render(request, 'news/add_new.html', context=data)


# Обработчик 'страница не найдена'
def pageNotFound(request, exception):
    return render(request, 'news/404.html')
