from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Account)
admin.site.register(Quater)
admin.site.register(Question)
admin.site.register(JoinQuater)
admin.site.register(Answer)

admin.site.site_header = 'Survey'
