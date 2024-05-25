from django.urls import path, re_path
from articles.views import articles


urlpatterns = [
    path('', articles.ArticleViewSet.as_view({
        'post': 'create',})),
    path('<int:pk>/', articles.ArticleViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    })),
    path('list/', articles.ArticleViewSet.as_view({'get': 'list'})),
]
