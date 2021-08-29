from django.db import models
from datetime import datetime, date, time
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Create your models here.
class advertisement(models.Model):
    title = models.CharField(max_length=120)
    one_day_date = models.DateField(default=date.today())
    start_time = models.TimeField(default=datetime.now())
    end_time = models.TimeField(default=datetime.now())
    start_date = models.DateField(default=date.today())
    end_date = models.DateField(default=date.today())
    number_of_hours = models.IntegerField(default=0)
    location_city = models.CharField(max_length=120)
    location_street = models.CharField(max_length=120)
    location_number = models.IntegerField()
    description = models.TextField()
    all_day = models.BooleanField(default=False)
    is_license = models.BooleanField(default=False)
    is_food = models.BooleanField(default=False)
    is_physical = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    # image = models.TextField() #todo: change to image field
#
#
# class v_userAccountManager(BaseUserManager):
#     def create_user(self, username, email, password, **other_fields):
#         user = self.model(username=username, email=self.normalize_email(email), **other_fields)
#         user.set_password(password)
#         user.save()
#         return user
#
#     def create_superuser(self, username, email, password, **other_fields):
#         other_fields.setdefault('is_staff', True)
#         other_fields.setdefault('is_superuser', True)
#         other_fields.setdefault('manager', True)
#         return self.create_user(username, email, password, **other_fields)


class v_user(models.Model):#AbstractBaseUser, PermissionsMixin
    username = models.CharField(max_length=120, unique=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.username
    # objects = v_userAccountManager()
    # USERNAME_FIELD = 'username'
    #
    # REQUIRED_FIELDS = ['email']
    #
    # def __str__(self):
    #     return self.username
    #
    # def has_perm(self, perm, obj=None):
    #     return self.is_superuser
    #
    # def has_module_perms(self, app_label):
    #     return True
