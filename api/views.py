from ntpath import join
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
import api.usable as uc
from .models import *
from passlib.hash import django_pbkdf2_sha256 as handler
import jwt 
import datetime
from decouple import config
from django.db.models import F

# Create your views here
class admin_login(APIView):
     def post(self,request):
        requireFields = ['email','password']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            email = request.data.get('email')
            password = request.data.get('password')

            fetchAccount = Account.objects.filter(email=email).first()
            if fetchAccount:
                if handler.verify(password,fetchAccount.password):
                    if fetchAccount.role == "admin":
                        access_token_payload = {
                                        'id': str(fetchAccount.uid),
                                        'name':fetchAccount.name, 
                                        'email':fetchAccount.email, 
                                        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=22),
                                        'iat': datetime.datetime.utcnow(),

                                }

                        access_token = jwt.encode(access_token_payload,config('adminkey'),algorithm = 'HS256')
                        data = {'uid':fetchAccount.uid,'name':fetchAccount.name,'email':fetchAccount.email,'contactno':fetchAccount.contactno,'designation':fetchAccount.designation,'stack':fetchAccount.stack,'role':fetchAccount.role }
                        
                        return Response({"status":True,"message":"Login Successlly","token":access_token,"admindata":data},200)

                    else:
                        return Response({"status":False,"message":"You are not login"})
                else:
                    return Response ({"status":False,"message":"Invalid crediatials"},200)
            else:
                return Response ({"status":False,"message":"Account doesnot access"},200)

                    # employee login
class employee_login(APIView):
    def post(self,request):
        requireFields = ['email','password']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                email = request.data.get('email')
                password = request.data.get('password')

                fetchAccount = Account.objects.filter(email=email).first()
                if fetchAccount:
                    if handler.verify(password,fetchAccount.password):
                        if fetchAccount.role == "employee":
                            access_token_payload = {
                                            'id': str(fetchAccount.uid),
                                            'name':fetchAccount.name, 
                                            'email':fetchAccount.email, 
                                            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=22),
                                            'iat': datetime.datetime.utcnow(),

                                    }

                            access_token = jwt.encode(access_token_payload,config('adminkey'),algorithm = 'HS256')
                            data = {'uid':fetchAccount.uid,'name':fetchAccount.name,'email':fetchAccount.email,'contactno':fetchAccount.contactno,'designation':fetchAccount.designation,'stack':fetchAccount.stack,'role':fetchAccount.role }
                            
                            return Response({"status":True,"message":"Login Successlly","token":access_token,"admindata":data},200)

                        else:
                            return Response({"status":False,"message":"You are not login"})
                    else:
                        return Response ({"status":False,"message":"Invalid crediatials"},200)
                else:
                    return Response ({"status":False,"message":"Account doesnot access"},200)
class encryptpass(APIView):
    def post(self,request):
        try:    
            passw = handler.hash(request.data.get('passw'))


            return HttpResponse(passw)

        except Exception as e:
            
            message = {'status':'Error','message':str(e)}
            return Response(message)