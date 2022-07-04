from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from user_management.models import Users


class UserRegSerializer(serializers.ModelSerializer):
    """用户注册序列化器


    """
    username = serializers.CharField(
        label="用户名",
        help_text="用户名",
        required=True,
        allow_blank=False,
        validators=[UniqueValidator(
            queryset=Users.objects.all(),
            message="用户已存在"
        )]
    )
    password = serializers.CharField(
        style={'input_type': 'password'},
        label='密码',
        write_only=True,
    )

    class Meta:
        model = Users
        fields = [
            'id',
            'password',
            'last_login',
            'email',
            'is_active',
            'phone_number',
            'department',
            'job',
            'profession',
            'name',
            'is_staff',
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详情序列化器

    """

    class Meta:
        model = Users
        fields = [
            'id',
            'last_login',
            'email',
            'is_active',
            'phone_number',
            'department',
            'job',
            'profession',
            'name',
            'is_staff',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'read_only': True},
            'last_login': {'read_only': True},
            'is_staff': {'read_only': True},
        }


class UserLoginSerializer(serializers.ModelSerializer):
    """用户登录序列化器

    """

    class Meta:
        model = Users
        fields = [
            'id',
            'username',
            'password',
        ]


class UserPasswordSerializer(serializers.ModelSerializer):
    """重置密码序列化器

    """
    new_password = serializers.CharField(
        max_length=128,
        min_length=8,
        allow_blank=False,
        trim_whitespace=True,
    )

    class Meta:
        model = Users
        fields = [
            'id',
            'username',
            'password',
            'new_password',
        ]
