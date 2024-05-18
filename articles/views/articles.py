from rest_framework import viewsets, views, status
from articles import models, serializers
from django.http.response import JsonResponse
from rest_framework.exceptions import PermissionDenied


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ArticleSerializer
    queryset = models.Article.objects.all()

    def list(self, request):
        # list of token roles
        print(request.roles)
        # Optional: get userinfo (SUB attribute from JWT)
        print(request.userinfo)

        return super().list(self, request)
