import email
from inspect import stack
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
import pandas as pd
import csv

# Create your views here

# ## ADMIN LOGIN API

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
                        JoinQuater(Accountid = fetchAccount).save()
                        
                        return Response({"status":True,"message":"Login Successlly","token":access_token,"admindata":data},200)

                    else:
                        return Response({"status":False,"message":"You are not login"})
                else:
                    return Response ({"status":False,"message":"Invalid crediatials"},200)
            else:
                return Response ({"status":False,"message":"Account doesnot access"},200)

# ## EMPLOYEE LOGIN API

class employee_login(APIView):
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
                    if fetchAccount.role == "employee":
                        access_token_payload = {
                                        'id': str(fetchAccount.uid),
                                        'name':fetchAccount.name, 
                                        'email':fetchAccount.email, 
                                        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=22),
                                        'iat': datetime.datetime.utcnow(),

                                }

                        access_token = jwt.encode(access_token_payload,config('employeekey'),algorithm = 'HS256')
                        data = {'uid':fetchAccount.uid,'name':fetchAccount.name,'email':fetchAccount.email,'contactno':fetchAccount.contactno,'designation':fetchAccount.designation,'stack':fetchAccount.stack,'role':fetchAccount.role }
                        JoinQuater(Accountid = fetchAccount).save()
                        
                        return Response({"status":True,"message":"Login Successlly","token":access_token,"employeedata":data},200)

                    else:
                        return Response({"status":False,"message":"You are not login"})
                else:
                    return Response ({"status":False,"message":"Invalid crediatials"},200)
            else:
                return Response ({"status":False,"message":"Account doesnot access"},200)

class EmployeeUpdate(APIView):
    def put (self,request):
        requireFields = ['uid','name','contactno','designation','stack']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else: 

            my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:

                uid = request.data.get('uid')
                role = request.data.get ('role')
                if role == 'employee':
                    checkaccount = Account.objects.filter(uid = uid).first()
                    if checkaccount:
                        checkaccount.name = request.data.get('name') 
                        checkaccount.contactno = request.data.get('contactno') 
                        checkaccount.designation = request.data.get('designation')
                        checkaccount.stack = request.data.get('stack')
                        checkaccount.save()
                        return Response({"status":True,"message":"Account Updated Successfully"})
                    else:
                        return Response ({"status":False,"message":"Account not found"})
                else:
                    return Response ({"status":False,"message":"Please Enter a correct account"})
            else:
                return Response ({"status":False,"message":"Unauthenticated"})

#DELETE EMPLOYEE ACCOUNT DATA
          
    def delete (self, request):
        my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            uid = request.GET['uid']
            data = Account.objects.filter(uid=uid).first()
            if data:
                data.delete()
                return Response({"status":True,"message":"Employee Account Deleted Successfully"})
            else:
                return Response({"status":False,"message":"Employee Account not Found"})
        else:
            return Response({"status":False,"message":"Unauthenticated"})

# GET EMPLOYEE ACCOUNT DATA
    
    def get (self,request): 
        my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            data = Account.objects.filter(role="employee").values('uid','name','contactno','email','designation','stack','role').order_by('-uid')
            return Response({"status":True,"data":data})
        else:
            return Response({"status":False,"message":"Unauthenticated"})

# GETSPECIFIC EMPLOYEE ACCOUNT DATA

class Getspecificemployeeaccount(APIView):
    def get(self, request):
        requireFields = ['uid']
        validator = uc.keyValidation(True,True,request.GET,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                uid = request.GET['uid']

                data = Account.objects.filter(uid = uid).values('uid','name','contactno','email','designation','stack').first()
                if data:
                    return Response({"status":True,"data":data})
                else:
                    return Response({"status":False,"message":"Data not found"})
class encryptpass(APIView):
    def post(self,request):
        try:    
            passw = handler.hash(request.data.get('passw'))


            return HttpResponse(passw)

        except Exception as e:
            
            message = {'status':'Error','message':str(e)}
            return Response(message)

# ## EMPLOYEE COUNT API

class employeeCount(APIView):
    def get(self,request):
        my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
                data = Account.objects.filter(role='employee').values('uid','name','email','contactno','designation','stack','role').count()
            
                return Response({"status":True,"data":data},200)
        else:
            return Response({"status":False,"message":'Unauthenticated'}),



# class uploadcsv(APIView):

#     def post (self,request): 
#             file = request.FILES.get("file")
#             if not file:
#                 return Response({'status':'warning','message':'File is required'})
            
#             if not file.name.endswith('csv'):
#                 return Response({'status':False,'message':"Your File Format is Incorrect"})

#             columnFormat = ['name','email','contactno','designation','stack','role']
#             convertDataFrame = pd.read_csv(file)
#             convertDataFrame = pd.DataFrame(convertDataFrame)
#             ###remove duplicate from upload file
#             bool_series = convertDataFrame["Model"].duplicated(keep = 'first')
#             convertDataFrame = convertDataFrame[~bool_series]# passing NOT of bool series to see unique values only

#             convertDataFrame.columns = [x.lower() for x in convertDataFrame.columns]
#             dataColumns = convertDataFrame.columns
#             if list(dataColumns) == columnFormat:
#                 name = convertDataFrame[columnFormat[0]]
#                 email = convertDataFrame[columnFormat[1]]
#                 contactno = convertDataFrame[columnFormat[2]]
#                 designation = convertDataFrame[columnFormat[3]]
#                 stack = convertDataFrame[columnFormat[4]]
#                 role= convertDataFrame[columnFormat[5]]

#                 bulklist = list()
#                 # for a,b,c,d,e,f,g,h,i in zip(name,email,contactno,designation,stack,role,):
#                 bulklist.append(Account(name=a,email=b,contactno=c,designation=d,stack=e,role=f))
#                 for a,b,c,d,e,f in zip(name,email,contactno,designation,stack,role):
#                     Account.objects.filter(Model=d).delete()  ###delete duplicate from database         
#                     bulklist.append(Account(name=a,email=b,contactno=c,designation=d,stack=e,role=f))
            
#                 Account.objects.bulk_create(bulklist)
#                 return Response({'status':True,'message':"Data Uploaded Successfully"})


#             else:
#                 return Response({'status':False,'message':"Your File Column Format is Incorrect"},)

class quaters(APIView):

# ## QUATER ADD API
    
    def post (self, request):
        requireFields = ['start_date','end_date','time']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                start_date = request.data.get ('start_date')
                end_date = request.data.get ('end_date')
                time = request.data.get ('time')

                data = Quater(start_date = start_date, end_date = end_date, time= time)

                data.save()

                return Response({"status":True,"message":"Quater Successfully Created"})
            else:
                return Response ({"status":False,"message":"Unauthenticated"})

# ## QUATER GET API

    def get (self, request):
        my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            data = Quater.objects.all().values('uid','start_date','end_date','time').order_by('-uid')
            
            return Response({"status":True,"data":data},200)
        else:
            return Response({"status":False,"message":'Unauthenticated'}),

# ## QUATER UPDATE API

    def put (self,request):
        requireFields = ['uid','start_date','end_date','time']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        else:
            my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                uid = request.data.get('uid')

                checkquater = Quater.objects.filter(uid = uid).first()
                if checkquater:
                    checkquater.start_date = request.data.get('start_date') 
                    checkquater.end_date = request.data.get('end_date') 
                    checkquater.time = request.data.get('time')

                    checkquater.save()
                    return Response({"status":True,"message":"Quater Updated Successfully"})
                else:
                    return Response({"status":True,"message":"Data not found"})
            else:
                return Response({"status":True,"message":"Unauthenticated"})

# ## QUATER DELETE API

    def delete(self,request):
        requireFields = ['uid']
        validator = uc.keyValidation(True,True,request.GET,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        else:
            my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                uid = request.GET['uid']
                data = Quater.objects.filter(uid=uid).first()
                if data:
                    data.delete()
                    return Response({"status":True,"message":"Account Deleted Successfully"})
                else:
                    return Response({"status":False,"message":"Account not Found"})
            else:
                return Response({"status":False,"message":"Unauthenticated"})

# ## QUATER GETSPECIFIC API

class Getspecificquater(APIView):
    def get (self,request):
        requireFields = ['uid']
        validator = uc.keyValidation(True,True,request.GET,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                uid = request.GET['uid']

                data = Quater.objects.filter(uid = uid).values('uid','uid','start_date','end_date','time').first()
                if data:
                    return Response({"status":True,"data":data})
                else:
                    return Response({"status":False,"message":"Data not found"})
class questions(APIView):
### QUESTION ADD API
    def post(self, request):
        requireFields = ['question','type','questiontype']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)

        else:
            my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                question = request.data.get ('question')
                type = request.data.get ('type')
                questiontype = request.data.get ('questiontype')

                data = Question(question = question, type = type, questiontype= questiontype)
                data.save()

                return Response({"status":True,"message":"Quater Successfully Created"})
            else:
                return Response ({"status":False,"message":"Unauthenticated"})

### QUESTION GET API

    def get (self,request):
        my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            data = Question.objects.all().values('uid','question','type','questiontype').order_by('-uid')
            
            return Response({"status":True,"data":data},200)
        else:
            return Response({"status":False,"message":'Unauthenticated'}),

### QUESTION UPDATE API

    def put (self,request):
        requireFields = ['uid','question','type','questiontype']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        else:
            my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                uid = request.data.get('uid')

                checkquestion = Question.objects.filter(uid = uid).first()
                if checkquestion:
                    checkquestion.question = request.data.get('question') 
                    checkquestion.type = request.data.get('type') 
                    checkquestion.questiontype = request.data.get('questiontype')

                    checkquestion.save()
                    return Response({"status":True,"message":"Question Updated Successfully"})
                else:
                    return Response({"status":True,"message":"Data not found"})
            else:
                return Response({"status":True,"message":"Unauthenticated"})

### QUESTION DELETE API

    def delete (self,request):
        requireFields = ['uid']
        validator = uc.keyValidation(True,True,request.GET,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        else:
            my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                uid = request.GET['uid']
                data = Question.objects.filter(uid=uid).first()
                if data:
                    data.delete()
                    return Response({"status":True,"message":"Question Deleted Successfully"})
                else:
                    return Response({"status":False,"message":"Data not Found"})
            else:
                return Response({"status":False,"message":"Unauthenticated"})


class answers(APIView):
### ANSWER ADD API

    def post (self,request):
        requireFields = ['answer','Qid']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)

        else:
            my_token = uc.employeetokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                answer = request.data.get ('answer')
                Qid = request.data.get ('Qid')

                getQid = Question.objects.filter(uid = Qid).first()
                
                data = Answer(answer = answer ,Qid = getQid)
                # JoinQuater(Quaterid = Quater)
                data.save()
                return Response({"status":True,"messsage":"Answer Can be successsfuuly added"})

### ANSWER GET API
    
    def get (self,request):
        my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            data = Answer.objects.all().values('uid','answer','Qid').order_by('-uid')
            
            return Response({"status":True,"data":data},200)
        else:
            return Response({"status":False,"message":'Unauthenticated'}),

### ANSWER UPDATE API

    def put (self, request):
        requireFields = ['uid','answer']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        else:
            my_token = uc.employeetokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                uid = request.data.get('uid')
                answer = request.data.get('answer')

                checkanswer = Answer.objects.filter(uid = uid).first()
                if checkanswer:
                    checkanswer.answer = request.data.get('answer') 

                    checkanswer.save()
                    return Response({"status":True,"message":"Question Updated Successfully"})
                else:
                    return Response({"status":True,"message":"Data not found"})
            else:
                return Response({"status":True,"message":"Unauthenticated"})

### ANSWER  DELETE API

    def delete (self, request):
        requireFields = ['uid']
        validator = uc.keyValidation(True,True,request.GET,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        else:
            my_token = uc.employeetokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                uid = request.GET['uid']
                data = Answer.objects.filter(uid=uid).first()
                if data:
                    data.delete()
                    return Response({"status":True,"message":"Answer  Deleted Successfully"})
                else:
                    return Response({"status":False,"message":"Answer not Found"})
            else:
                return Response({"status":False,"message":"Unauthenticated"})

### ANSWER  GETSPECIFIC API

class Getspecificanswer (APIView):
    def get(self, request):
        requireFields = ['uid']
        validator = uc.keyValidation(True,True,request.GET,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                uid = request.GET['uid']

                data = Answer.objects.filter(uid = uid).values('uid','answer','Qid').first()
                if data:
                    return Response({"status":True,"data":data})
                else:
                    return Response({"status":False,"message":"Data not found"})
                
    
# class joinquaters(APIView):
#     def get (self,request):
        