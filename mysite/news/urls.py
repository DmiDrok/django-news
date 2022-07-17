from django.urls import path

from .views import index, contact
from .views import NewsAll, NewsCat, NewOne, NewAdd, RegisterUser, LoginUser, logout_user

from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(index), name='index'),
    path('news/', cache_page(60)(NewsAll.as_view()), name='all_news'),
    path('new/<slug:new_slug>/', NewOne.as_view(), name='new'),
    path('news_by_cats/<slug:cat_slug>', cache_page(60)(NewsCat.as_view()), name='news_by_cat'),
    path('add_new/', NewAdd.as_view(), name='add_new'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('authorization/', LoginUser.as_view(), name='auth'),
    path('logout/', logout_user, name='logout_user'),
    path('contact/', contact, name='contact'),
]