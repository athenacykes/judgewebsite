from rest_framework import viewsets, views, status
from articles import models, serializers
from django.http.response import JsonResponse
from rest_framework.exceptions import PermissionDenied


class ArticleViewSet(viewsets.ModelViewSet):
    """
    Bank endpoint
    This endpoint has all configured keycloak roles
    """
    serializer_class = serializers.ArticleSerializer
    queryset = models.Article.objects.all()

    def list(self, request):
        """
        Overwrite method
        You can specify your rules inside each method
        using the variable 'request.roles' that means a
        list of roles that came from authenticated token.
        See the following example bellow:
        """
        # list of token roles
        print(request.roles)

        # Optional: get userinfo (SUB attribute from JWT)
        print(request.userinfo)

        return super().list(self, request)
