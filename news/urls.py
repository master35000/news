from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, PostCreate, PostUpdate, PostDelete, NewsSearch



urlpatterns = [
   path('', NewsList.as_view(), name='post_list'),
   path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
   path('search', NewsSearch.as_view(), name='news_search'),
   path('news/create/', PostCreate.as_view(), name='post_create'),
   path('articles/create/', PostCreate.as_view(), name='post_create'),
   path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   ]

