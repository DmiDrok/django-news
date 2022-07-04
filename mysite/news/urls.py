from django.urls import path

from .views import index, all_news, new, news_by_cat


urlpatterns = [
    path('', index, name='index'),
    path('news/', all_news, name='all_news'),
    path('new/<int:new_id>/', new, name='new'),
    path('news_by_cats/<int:cat_id>', news_by_cat, name='news_by_cat')
]