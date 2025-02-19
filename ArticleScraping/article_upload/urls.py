from django.urls import path
from .views import article_list, upload_article

urlpatterns = [
    path('', article_list, name='article_list'),
    path('upload/', upload_article, name='upload_article'),
]
