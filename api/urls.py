from django.urls import path,include
from api.views import *

urlpatterns = [

#web urls  home
path('',admin_login.as_view()),
path('admin_login',admin_login.as_view()),
path('employee_login',employee_login.as_view()),
path('encryptpass',encryptpass.as_view()),
]