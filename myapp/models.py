from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.
class User_Profile(models.Model):

    user         = models.OneToOneField(User,on_delete=models.CASCADE)
    name         = models.CharField(max_length=140, null=True,default="User")
    phone_number = models.CharField(unique=True,max_length=10)
    age          = models.CharField(max_length=3)
    gender       = models.CharField(max_length=10,null=True,)
    user_image   = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100,)

    def __str__(self):
        return self.name

class Category(models.Model):
    name  = models.CharField(max_length=130)
    
    def __str__(self):
        return self.name

class Blog(models.Model): 
     blog_title     = models.CharField(max_length=225)
     blog_contant   = RichTextField(null=True)
     blog_create_on = models.DateTimeField(auto_now_add=True)
     blog_last_edit = models.DateTimeField(auto_now=True)
     blog_draft     = models.BooleanField(default=False)
     blog_img       = models.ImageField(upload_to='blog_images')
     blog_Category  = models.ForeignKey(Category,on_delete=models.CASCADE)
     like           = models.IntegerField(default=0)
     user_profile   = models.ForeignKey(User_Profile,on_delete=models.CASCADE)

     def __str__(self):
           return self.blog_title

class Comment(models.Model):
     parent         = models.ForeignKey("self",on_delete=models.SET_NULL,null=True,blank=True,) 
     text_comment   = models.CharField(max_length=300)
     post           = models.ForeignKey(Blog, on_delete=models.CASCADE)
     commented_by   = models.ForeignKey(User_Profile, related_name="Comment",on_delete=models.CASCADE,null=True,blank=True)
     by_Reply       = models.ForeignKey(User_Profile,related_name="replies", on_delete=models.CASCADE,null=True,blank=True)
     created_at     = models.DateTimeField(auto_now_add=True)  
     updated_at     = models.DateTimeField(auto_now=True) 
     


class Likes(models.Model):  
     
     blog          = models.ForeignKey(Blog,on_delete=models.CASCADE)
     user_Profile  = models.ForeignKey(User,on_delete=models.CASCADE)
    
