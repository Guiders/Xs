from django.db import models


# Create your models here.
# class UserProfile(AbstractUser):
#     """
#     用户
#     """
#     name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
#     birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
#     gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", u"女")), default="female",
#                               verbose_name="性别")
#     mobile = models.CharField(max_length=11, verbose_name="电话")
#     email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")
#
#     class Meta:
#         verbose_name = '用户'
#         verbose_name_plural = '用户'
#
#     def __str__(self):
#         return self.username


class TestModel(models.Model):
    name = models.CharField(max_length=30, null=True, verbose_name="名称")
    moblie = models.CharField(max_length=11, verbose_name="电话")
