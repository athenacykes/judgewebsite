from django.db import models
from users.models import SystemUser, UserCriteriaSet
from common.models import BaseModel


# Create your models here.
class Forum(BaseModel):
    title = models.CharField(max_length=100)
    cover_pic = models.ImageField(upload_to='media/upload/', null=True, blank=True)
    short_description = models.CharField(max_length=200)
    description = models.TextField()
    parent_forum = models.ForeignKey('self', on_delete=models.DO_NOTHING, db_constraint=False,
                                     null=True, blank=True, default=None)
    moderators = models.ManyToManyField(SystemUser)
    visibility = models.ManyToManyField(UserCriteriaSet)

    def evaluate_visibility(self, user):
        for criteria_set in self.visibility.all():
            if criteria_set.evaluate(user):
                return True
        return False


class Thread(BaseModel):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(SystemUser, on_delete=models.DO_NOTHING, db_constraint=False)
    reply_to = models.ForeignKey('self', on_delete=models.DO_NOTHING, db_constraint=False,
                                 null=True, blank=True, default=None)
    is_sticky = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

