from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(User_Profile)
admin.site.register(Category)
admin.site.register(Blog)
admin.site.register(Comment)    
admin.site.register(Likes)
