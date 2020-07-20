from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication
from rest_framework.authentication import get_authorization_header, exceptions
from django.contrib.auth.models import AnonymousUser
"""
如果要針對 專案api 判定user 身份驗證就從這邊改寫 
"""
