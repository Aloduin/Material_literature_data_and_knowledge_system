# import logging
# import random
# import string
#
# import django.conf
# from django.contrib.auth import get_user_model
# from django.shortcuts import get_object_or_404
# from django.http import HttpResponse, JsonResponse
# from django.contrib.auth import authenticate, login, logout as auth_logout
# from django.contrib.auth.hashers import make_password
# from django.contrib.auth.models import AnonymousUser
# from django.contrib.sites.models import Site
# from django.core.mail import send_mail
# from django.urls import reverse
# from django.db.models import QuerySet
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import viewsets, permissions, status
# from rest_framework import serializers
# from rest_framework.exceptions import ValidationError
# from rest_framework.generics import GenericAPIView
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from user_management.models import Users
# from user_management.serializers import UserRegSerializer, UserDetailSerializer, UserLoginSerializer
# from user_management.serializers import UserPasswordSerializer
#
# # Create your views here.
#
# logger = logging.getLogger(__name__)
#
#
# def get_random_password() -> string:
#     """生成随机字符密码.
#
#     用于生成8位随机的密码.
#     :return: 8位随机字符密码.
#     """
#     return ''.join(random.sample(string.ascii_letters + string.digits, 8))
#
#
# class BaseError(ValidationError):
#     def __init__(self, detail=None, code=None):
#         super(BaseError, self).__init__(detail={'detail': detail})
#
#
# class BaseViewSetMixin(object):
#     filter_backends = [DjangoFilterBackend]
#     permissions_classes = [permissions.IsAuthenticated]
#
#     def __init__(self, **kwargs) -> None:
#         self.filter_set_fields = []
#         self.init_filter_field()
#
#     def init_filter_field(self):
#         serializer = self.get_serializer_class()
#
#         if not hasattr(serializer, 'Meta'):
#             return
#         meta = serializer.Meta
#
#         if not hasattr(meta, 'model'):
#             return
#         model = meta.model
#
#         if not hasattr(meta, 'field'):
#             ser_fields = []
#         else:
#             ser_fields = meta.fields
#
#         for field in ser_fields:
#             if not hasattr(model, field):
#                 continue
#             self.filter_set_fields.append(field)
#
#     def perform_update(self, serializer):
#         user = self.fill_user(serializer, 'update')
#         return serializer.save(**user)
#
#     def perform_create(self, serializer):
#         user = self.fill_user(serializer, 'create')
#         return serializer.save(**user)
#
#     @staticmethod
#     def fill_user(serializer: serializers, mode: string) -> dict:
#         request = serializer.context['request']
#         user_id = request.user.id
#         ret = {
#             'modifier': user_id
#         }
#         if mode == 'create':
#             ret['creator'] = user_id
#
#         return ret
#
#     def get_pk(self):
#         if hasattr(self, 'kwargs'):
#             return self.kwargs.get('pk')
#
#     def is_reader(self):
#         return isinstance(self.request.user, AnonymousUser) or not self.request.user.is_staff
#
#
# class BaseModelViewSet(BaseViewSetMixin, viewsets.ModelViewSet):
#     pass
#
#
# class UserViewSet(BaseViewSetMixin, viewsets.ModelViewSet):
#     """用户注册视图类
#
#     """
#     filter_backends = [DjangoFilterBackend]
#     queryset = Users.objects.all().order_by('username')
#     serializers_class = UserRegSerializer
#     permissions_classes = [permissions.AllowAny]
#
#     def filter_queryset(self, queryset):
#         queryset = super(UserViewSet, self).filter_queryset(queryset)
#         return queryset
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         raw_password = serializer.validated_data['password']
#         user = self.perform_create(serializer)
#         user.set_password(raw_password)
#         user.is_active = False
#         user.save()
#         re_dict = serializer.data
#         site = get_current_site().domain
#         sign = get_sha256(get_sha256(settings.SECRET_KEY + str(user.id)))
#
#         if settings.DEBUG:
#             site = '127.0.0.1:8000'
#         path = reverse('result')
#         url = "http://{site}{path}?type=validation&id={id}&sign={sign}".format(
#             site=site, path=path, id=user.id, sign=sign)
#         content = """
#                         <p>请点击下面链接验证您的邮箱</p>
#                         <a href="{url}" rel="bookmark">{url}</a>
#                         再次感谢您！
#                         <br />
#                         如果上面链接无法打开，请将此链接复制至浏览器。
#                         {url}
#                         """.format(url=url)
#         try:
#             """
#             send_mail(subject="验证您的电子邮箱",
#                     message=content,
#                     from_email=django.conf.settings.EMAIL_HOST_USER,
#                     recipient_list=[user.email],
#                     fail_silently=False)
#             """
#             sendMailTask.delay(subject="验证您的电子邮箱",
#                                message=content,
#                                recipient_list=[user.email])
#
#             re_dict["detail"] = "向你的邮箱发送了一封邮件，请打开验证，完成注册。"
#         except Exception as e:
#             print(e)
#             re_dict["detail"] = "发送验证邮箱失败，请检查邮箱是否正确。"
#
#         headers = self.get_success_headers(serializer.data)
#         return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)
#
#
# class UserLoginViewSet(GenericAPIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = UserLoginSerializer
#     queryset = Users.objects.all()
#
#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username', '')
#         password = request.data.get('password', '')
#         # for test serializer class
#         # print(request.data)
#         # serializer = self.get_serializer(data=request.data)
#         # serializer.is_valid(raise_exception=True)
#         # print(serializer.validated_data)
#
#         users = Users.objects.filter(username=username)
#         user: Users = users[0] if users else None
#         if user is None:
#             return Response({'detail': '用户不存在。'}, status=status.HTTP_200_OK)
#         if not user.is_active:
#             return Response({'detail': '账号未激活，请登录邮箱激活。'}, status=status.HTTP_200_OK)
#
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 serializer = UserDetailSerializer(user)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             ret = {'detail': '密码错误或验证失败。'}
#             return Response(ret, status=status.HTTP_200_OK)
#
#
# class UserLogoutViewSet(GenericAPIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = UserLoginSerializer
#
#     def get(self, request, *args, **kwargs):
#         auth_logout(request)
#         return Response({'detail': 'logout successful!'})