from django.db import models
from django.contrib.auth.models import User
from common.models import BaseModel


# Create your models here.
class Article(BaseModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False)

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"
