from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class AbstractBaseModel(models.Model):
    """定义用户基类。

    该抽象基类定义了一些用户的基本信息。
    未来可基于此类来实现角色管理。

    """
    phone_number = models.CharField(
        max_length=11,
        verbose_name="电话号码",
        help_text="11位中国手机号码，允许为空",
        null=True,
        blank=True,
    )
    department = models.CharField(
        max_length=30,
        verbose_name="单位",
        help_text="单位名称，30个字符以内，允许为空",
        null=True,
        blank=True,
    )
    job = models.CharField(
        max_length=20,
        verbose_name="职业",
        help_text="职业名称，20个字符以内，允许为空",
        null=True,
        blank=True,
    )
    profession = models.CharField(
        max_length=10,
        verbose_name="职称/学位",
        help_text="职称或学位名称，10个字符以内，允许为空",
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=30,
        verbose_name="真实姓名",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class Users(AbstractUser, AbstractBaseModel):
    class Meta:
        db_table = "db_Users"
        swappable = 'AUTH_USER_MODEL'
