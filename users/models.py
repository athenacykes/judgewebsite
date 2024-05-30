from django.db import models
from django.apps import apps
from django.contrib.auth.models import User
from common.models import BaseModel


class SystemUser(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


class InvitationCode(BaseModel):
    code = models.CharField(max_length=20, unique=True)
    is_used = models.BooleanField(default=False)
    created_by = models.ForeignKey(SystemUser, on_delete=models.DO_NOTHING, db_constraint=False)
    used_by = models.ForeignKey(SystemUser, on_delete=models.DO_NOTHING, db_constraint=False, null=True, blank=True)

    # automatically generate a new code on create
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super(InvitationCode, self).save(*args, **kwargs)

    def generate_code(self):
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
    
    @classmethod
    def get_validate_code(cls, code):
        try:
            invitation_code = cls.objects.get(code=code)
            if not invitation_code.is_used:
                return invitation_code
        except cls.DoesNotExist:
            pass
        return None


# Create your models here.
class MTGJudgeUser(BaseModel):
    judge_user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=10)
    region = models.CharField(max_length=10)


class UserContact(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    province = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    wechat = models.CharField(max_length=50, null=True, blank=True)
    qq = models.CharField(max_length=12, null=True, blank=True)


class UserPreference(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    show_email = models.BooleanField(default=False)
    show_mobile = models.BooleanField(default=False)
    show_wechat = models.BooleanField(default=False)
    show_qq = models.BooleanField(default=False)


class UserCriteria(BaseModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    app_name = models.CharField(max_length=50)
    model_name = models.CharField(max_length=50)
    field_name = models.CharField(max_length=50)
    field_type = models.CharField(max_length=50)
    field_value = models.CharField(max_length=50)

    def evaluate(self, obj):
        # Evaluate if the object meets the criteria
        app = apps.get_app_config(self.app_name)
        model = app.get_model(self.model_name)
        field = getattr(model, self.field_name)
        value = field(obj)
        if self.field_type == 'eq':
            return str(value) == self.field_value
        elif self.field_type == 'ne':
            return str(value) != self.field_value


class UserCriteriaSet(BaseModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    criteria = models.ManyToManyField(UserCriteria)

    def evaluate(self, obj):
        # Evaluate if the object meets the one of the criteria in set
        for criteria in self.criteria.all():
            if criteria.evaluate(obj):
                return True
