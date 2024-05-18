from django.urls import path, re_path
from articles.views import articles


urlpatterns = [
    path('list', articles.ArticleViewSet.as_view({'get': 'list'})),
]
