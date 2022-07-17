from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.views.decorators.cache import cache_page
from django.core.cache import cache


from .models import New, Category
from .forms import AddNewForm, RegisterUserForm, LoginUserForm, ContactForm
from .utils import DataMixin

import math


# Обработчик главной страницы
# @login_required(login_url='/admin/')
# @cache_page(60)
def index(request):
    print(request.GET)
    active = 'index'
    data = {
        'active': active,
    }


    return render(request, 'news/index.html', context=data)


# # Обработчик новостей
# def all_news(request, num_page):
#     if num_page == 0:
#         return redirect('all_news', 1)
#     else:
#         now_page = num_page - 1
#         news = New.objects.filter(is_published=True)[now_page * 3:now_page * 3 + 3]
#
#     all_news = New.objects.filter(is_published=True)
#     paginate_pages = None  # Тут будет количество всех страниц
#     if len(all_news) > 3:  # Если количество опубликованных новостей больше 3 - то делаем пагинацию
#         paginate_pages = range(1, math.ceil((len(all_news) // 3 + 1)) + 1)
#
#     active = 'all_news'
#     data = {
#         'news': news,
#         'active': active,
#         'paginate_pages': paginate_pages,
#         'num_page': num_page,
#     }
#
#
#     return render(request, 'news/all_news.html', context=data)

class NewsAll(DataMixin, ListView):
    model = New
    template_name = 'news/all_news.html'
    context_object_name = 'news'
    all_news = model.objects.filter(is_published=True)
    allow_empty = False
    paginate_by = 3


    # Получить контекст
    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(active='all_news')
        #context['paginate_pages'] = range(1, math.ceil((len(self.all_news) // 3 + 1)) + 1) if len(self.all_news) > 3 else None
        #context['num_page'], context['news'] = self.get_num_page_and_news()

        context.update(c_def)

        return context

    # Получить queryset (меняем под свои условия возвращаемый ListView результат)
    def get_queryset(self):
        return self.model.objects.filter(is_published=True).select_related('cat')

    # Получить текущую страницу и новости для текущей страницы
    def get_num_page_and_news(self):
        self.num_page = self.kwargs['num_page']

        if self.num_page == 0:
            return None, None
        else:
            now_page = self.num_page - 1
            news = New.objects.filter(is_published=True)[now_page * 3:now_page * 3 + 3]


        return self.num_page, news


# # Обработчик одной новости
# def new(request, new_slug):
#     new = get_object_or_404(New, slug=new_slug, is_published=True)
#     cats = Category.objects.all()[:5]
#     active = 'all_news'
#
#     data = {
#         'new': new,
#         'active': active,
#         'cats': cats,
#     }
#
#     return render(request, 'news/new.html', context=data)


class NewOne(DataMixin, DetailView):
    model = New
    template_name = 'news/new.html'
    slug_url_kwarg = 'new_slug'
    context_object_name = 'new' # Название приложения тут стоит и по умолчанию. Мы можем определить что угодно, главное - совпадение с переменной в шаблоне


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(active='all_news')
        context.update(c_def)

        return context

    def get_queryset(self):
        return self.model.objects.filter(slug=self.kwargs['new_slug'], is_published=True)


# Обработчик новостей по категориям
# def news_by_cat(request, cat_slug):
#     news = New.objects.filter(cat__slug=cat_slug, is_published=True)
#     cat_name = news[0].cat.name
#
#     active = 'all_news'
#
#     data = {
#         'news': news,
#         'active': active,
#         'cat_name': cat_name,
#     }
#
#     return render(request, 'news/news_by_cat.html', context=data)


class NewsCat(DataMixin, ListView):
    model = New
    template_name = 'news/news_by_cat.html'
    context_object_name = 'news'
    allow_empty = True
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(active='all_news', cat_name=Category.objects.get(slug=self.kwargs['cat_slug']).name)
        context.update(c_def)

        return context

    def get_queryset(self):
        return self.model.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')


# Обработчик добавления новости
# def add_new(request):
#     active = 'add_new'
#
#     if request.method == 'POST':
#         form = AddNewForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     else:
#         form = AddNewForm()
#
#     data = {
#         'active': active,
#         'form': form,
#     }
#
#     return render(request, 'news/add_new.html', context=data)

class NewAdd(DataMixin, LoginRequiredMixin, CreateView):
    form_class = AddNewForm
    template_name = 'news/add_new.html'
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('index')
    # raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(active='add_new')
        context.update(c_def)

        return context


# Класс представления для обработки формы регистрации
class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'news/register.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

# Класс представления для обработки формы авторизации
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'news/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def logout_user(request):
    logout(request)
    return redirect('index')


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form = ContactForm()
    else:
        form = ContactForm()

    return render(request, 'news/contact.html', {'form': form, 'active': 'contact'})


# Обработчик 'страница не найдена'
def pageNotFound(request, exception):
    return render(request, 'news/404.html')
