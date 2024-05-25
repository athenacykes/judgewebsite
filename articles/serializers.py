from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()
    created_time = serializers.DateTimeField(required=False)

    class Meta:
        model = Article
        fields = '__all__'
