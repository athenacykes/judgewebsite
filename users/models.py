from django.db import models
from django.contrib.auth.models import User
from common.models import BaseModel


# Create your models here.
class MTGJudgeUser(BaseModel):
    judge_user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=10)
    region = models.CharField(max_length=10)
