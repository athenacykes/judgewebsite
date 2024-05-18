from rest_framework import serializers


class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()
    created_time = serializers.DateTimeField()
