from django.db import models
import uuid


# Create your models here.
types = (
    ("description","description"),
    ("multiplecoices","multiplecoices"),
)
role = (
    ('admin','admin'),
    ('employee','employee'),
)

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    class Meta:
        abstract = True
        
class Account(BaseModel):
    name = models.CharField(max_length=255, default='')
    email = models.EmailField(max_length=255, default='')
    password = models.TextField(default='')
    contactno = models.CharField(max_length=255, default='')
    designation = models.CharField(max_length=255, default='')
    stack = models.CharField(max_length=255, default='')
    role = models.CharField(choices=role,max_length=20,default="employee")

class Quater (BaseModel):
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    status = models.BooleanField(default=False)

class Question(BaseModel):
    question = models.TextField(default="")
    type = models.CharField(choices=types,max_length=200,default="description")
    questiontype  = models.TextField(default='')

class JoinQuater(BaseModel):
    Accountid = models.ForeignKey(Account,on_delete=models.CASCADE,blank=True,null=True)
    Quaterid = models.ForeignKey(Quater,on_delete=models.CASCADE,blank=True,null=True)
    status = models.BooleanField(default=False)

class Answer(BaseModel):
    answer = models.TextField(default="")
    Qid = models.ForeignKey(Question,on_delete=models.CASCADE,blank=True,null=True)
    