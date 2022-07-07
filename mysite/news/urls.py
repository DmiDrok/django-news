from django.urls import path

from .views import index, all_news, new, news_by_cat, add_new


urlpatterns = [
    path('', index, name='index'),
    path('news/<int:num_page>/', all_news, name='all_news'),
    path('new/<slug:new_slug>/', new, name='new'),
    path('news_by_cats/<slug:cat_slug>', news_by_cat, name='news_by_cat'),
    path('add_new/', add_new, name='add_new'),
]