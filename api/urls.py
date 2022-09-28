from django.urls import path,include
from api.views import *

urlpatterns = [

#web urls  home
path('',admin_login.as_view()),
path('admin_login',admin_login.as_view()),
path('employee_login',employee_login.as_view()),
path('encryptpass',encryptpass.as_view()),
path('employeeCount',employeeCount.as_view()),
# path('uploadcsv',uploadcsv.as_view()),
path('quaters',quaters.as_view()),
path('Getspecificquater',Getspecificquater.as_view()),
path('questions',questions.as_view()),
path('answers',answers.as_view()),
path('Getspecificanswer',Getspecificanswer.as_view()),
path('EmployeeAdd',EmployeeAdd.as_view()),
path('Getspecificemployeeaccount',Getspecificemployeeaccount.as_view()),
]