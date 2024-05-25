from rest_framework import viewsets, views, status
from articles import models, serializers
from django.http.response import JsonResponse
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
import base64
import json


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ArticleSerializer
    queryset = models.Article.objects.all()
    pagination_class = PageNumberPagination

    def list(self, request):
        # list of token roles
        print(request.roles)
        # Optional: get userinfo (SUB attribute from JWT)
        print(request.userinfo)

        # accepts parameter filter which is json encapsulates in base64 to filter the article list
        filter = request.query_params.get('filter', None)
        # decodes base64
        if filter:
            filter = base64.b64decode(filter).decode('utf-8')
            filter = json.loads(filter)
        else:
            filter = {}
        # accepts parameter uid to filter the article list by author
        uid = request.query_params.get('uid', None)
        if uid:
            filter = {'author': uid}
        # applies all the parameter to the queryset
        queryset = self.get_queryset().filter(**filter)
        pagination = PageNumberPagination()
        page = pagination.paginate_queryset(queryset, request)
        serializer = self.serializer_class(page, many=True)
        return pagination.get_paginated_response(serializer.data)
