from rest_framework.permissions import BasePermission
from functools import partial
from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication
from rest_framework.authentication import get_authorization_header, exceptions
from django.contrib.auth.models import AnonymousUser
"""
如果除了厭戰身份外還需要驗證該使用者是不是有此權限就會用這個
"""