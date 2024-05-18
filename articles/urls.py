from django.urls import path, re_path
from articles.views import articles


urlpatterns = [
    path('<int:pk>/', articles.ArticleViewSet.as_view({
        'get': 'retrieve',
        'post': 'create',
        'put': 'update',
        'delete': 'destroy',
    })),
    path('list', articles.ArticleViewSet.as_view({'get': 'list'})),
]
