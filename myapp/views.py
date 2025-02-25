from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from . models import  *
from django .shortcuts import HttpResponseRedirect
from django.urls import reverse
from  django.contrib import messages
from django.contrib.auth.models import  User
from django.contrib.auth import authenticate ,login,logout
from django.contrib.auth.decorators  import login_required
from django.core.files.storage import FileSystemStorage



# Create your views here.
def home(request):
     get_blog   =  Blog.objects.filter(blog_draft=False)
     get_like   =  Likes.objects.all().count()
     context    = {"blog_details":get_blog,
                    "likes"      :get_like,
                    }     
     return render(request,"home.html",context)

def signup(request):
    if request.method=="POST":
        username     = request.POST.get("username")
        first_name   = request.POST.get("firstname").lower()
        last_name    = request.POST.get("lastname").lower()
        email        = request.POST.get("email").lower()
        phone_number = request.POST.get("phonenumber")
        age          = request.POST.get("age")
        gender       = request.POST.get("gender")
        password     = request.POST.get("password")
        image        = request.POST.get("image")
        
        if (User.objects.filter(username=username).exists() or
            User.objects.filter(email=email).exists() or
            User_Profile.objects.filter(phone_number=phone_number).exists()
             ):
                messages.warning(request,"User already exists ")       
        else :
             data = User.objects.create(username=username,
                                      email=email,
                                      first_name=first_name,
                                      last_name=last_name)
             data.set_password(password)
             data.save()
             User_Profile.objects.create(user=data,
                                         user_image=image,
                                         name=f'{first_name}{ last_name}',
                                         phone_number=phone_number,
                                         gender=gender,age=age)
             messages.success(request,f'Successfully Create user :- {first_name} {last_name}' ) 
             return redirect('signin') 

    return render(request,"sign_up.html")

def signin(request):
      if request.method=="POST":        
            email    = request.POST.get("email")
            password = request.POST.get("password")
            
            try:
                    try:
                            get_phone = User_Profile.objects.get(phone_number=email)
                            user      = authenticate(request,username=get_phone.user.username,password=password)          
                    except:
                           get_email = User_Profile.objects.get(user__email = email.lower())         
                           user      = authenticate(request,username=get_email.user.username,password=password)            
            except:
                       user=authenticate(request,username=email,password=password)
            if user is not None:
                            login(request,user)
                          
                            return redirect('dashbord')      
            else:
                            messages.warning(request,f'Wrong password  try Again ')
                                    
            
                  
      return render(request,"sign_in.html")

def signout(request):
     logout(request)
     return redirect("home")

@login_required
def dashbord(request):
       get_object =  User_Profile.objects.filter(user = request.user)
       get_blog   =  Blog.objects.filter(blog_draft=False).order_by("-blog_create_on")
       
       context    =  {  "user_info" : get_object,
                      
                        "blog_data" : get_blog, 
                               
                    }
      
       return render(request,'Dashbord.html',context)


def userprofile(request):
   get_user_info=User_Profile.objects.filter(user=request.user)
   context={"user_info":get_user_info}
   return render(request,"profile.html",context)

def editprofile(request, id):
    get_data     = get_object_or_404(User_Profile, id=id)
    getUser_data = get_data.user
    user_info    = User_Profile.objects.filter(id = id)
    context      = {'user_info': user_info}

    if request.method == 'POST' and request.FILES.get("image"):

               usernamec     = request.POST.get("username", "").strip()
               first_namec   = request.POST.get("firstname", "").strip().lower()
               last_namec    = request.POST.get("lastname", "").strip().lower()
               emailc        = request.POST.get("email", "").strip().lower()
               phone_numberc = request.POST.get("phonenumber", "").strip()
               agec          = request.POST.get("age", "").strip()
               genderc       = request.POST.get("gender", "").strip()
               imagec        = request.FILES["image"]
              
              


               if not usernamec or not first_namec or not last_namec or not emailc or not phone_numberc or not agec or not genderc:
                    messages.warning(request, "All fields are mandatory.")
                    return redirect("editprofile",id)
               

               
               if usernamec != getUser_data.username and User.objects.filter(username=usernamec).exclude(id=getUser_data.id).exists():
                    messages.warning(request, f"Username '{usernamec}' is already in use.")
                    return redirect('editprofile',id)

               
               if emailc != getUser_data.email and User.objects.filter(email=emailc).exclude(id=getUser_data.id).exists():
                    messages.warning(request, f"Email '{emailc}' is already in use.")
                    return redirect("editprofile",id)

               
               if phone_numberc != get_data.phone_number and User_Profile.objects.filter(phone_number=phone_numberc).exclude(id=get_data.id).exists():
                    messages.warning(request, f"Phone number '{phone_numberc}' is already in use.")
                    return redirect('editprofile')

               
               getUser_data.username   = usernamec
               getUser_data.email      = emailc
               getUser_data.first_name = first_namec
               getUser_data.last_name  = last_namec
               getUser_data.save()

               # Update profile data
               get_data.gender       = genderc
               get_data.name         = f"{first_namec} {last_namec}"
               get_data.phone_number = phone_numberc
               get_data.age          = agec
               fs                    = FileSystemStorage()
               filename              = fs.save(imagec.name, imagec)
               get_data.user_image   =f"uploads/{filename}"
               get_data.save()
               return redirect("userprofile")

    return render(request, "userprofileedit.html", context)

def yourblog(request,user_id):
      user  = User_Profile.objects.filter( id = user_id)
      post  = Blog.objects.filter(user_profile__id = user_id).order_by('-blog_create_on')
      context = {
                  "user"         : user,
                  "blog_content" : post
                }
      
     
      return render(request,"yourblog.html",context)
       


def changepassword(request,id):
     get_user      =  get_object_or_404(User_Profile, id = id)
     getUser_info  = get_user.user 
     context       = {"get_user_info":User_Profile.objects.filter(id = id)}
     if request.method == "POST":
           password         = request.POST.get("Password")
           confirm_password = request.POST.get('ConfirmPassword')
           if password != confirm_password:
                 messages.warning(request,f" No matched password !")
           else:
                 getUser_info.set_password(confirm_password)
                 getUser_info.save()
                 return redirect("signout") 

     return render(request,"changepassword.html",context)


def add_category(request):
       if request.method == "POST":
              category_field = request.POST.get("add_category")
              if category_field != "":
                Category.objects.create(name=category_field)
                return redirect('Write_Blog')
              else:
                messages.warning(request,f'Not allow')
       context= User_Profile.objects.filter(user=request.user)
       return render(request,'add_category.html',{"context":context})


def Write_Blog(request):
        get_category = Category.objects.all()
        get_user     = User_Profile.objects.filter(user = request.user)
        user_profile = User_Profile.objects.get(user = request.user)
        context      = {"category":get_category,
                        "user_info": get_user,
                        }
        print("1")
        if request.method == "POST" and "image" in request.FILES:
                print("2")
                blog_title   = request.POST.get('blogtitle')
                category     = Category.objects.get(name = request.POST.get("blog_category"))
                
                blog_content = request.POST.get('Content')
                blog_image   =  request.FILES["image"]

                is_draft     = request.POST.get('checkbox')
                print(blog_image,"we were here.........")
               
                if is_draft is None:
                    is_draft= False
                else :
                    is_draft = True
                if not blog_content or not blog_image or not blog_title:
                        messages.warning(request,f"  Not allow this action !")
                else:
                        print("23")
                        fs = FileSystemStorage()
                        print("24")
                        filename = fs.save(blog_image.name, blog_image)
                        print("25")

                        Blog.objects.create(
                               
                                 blog_title    = blog_title,
                                 blog_contant  = blog_content,
                                 
                                 blog_img      = f"uploads/{filename}",
                                 user_profile  = user_profile,
                                 blog_Category = category,
                                 blog_draft    = is_draft
                                 ) 
                        print("im here....")
                       
                        return redirect('dashbord')

      
        return render(request,'createblog.html',context)

@login_required
def viewblog(request,id):
       get_user_data = User_Profile.objects.filter(user=request.user)
       get_blog      = Blog.objects.filter(id=id)
       
       get_comment   = Comment.objects.filter(post__id = id,by_Reply = None )
       
       context       = {
                         "blog_content"     : get_blog,
                         "customer_details" : get_user_data,
                         "comment"          : get_comment
                          
                          }
       
       return  render (request,'showblog.html',context) 
           

def draft_show(request):
        get_draft = Blog.objects.filter(blog_draft = True)
        get_user  = User_Profile.objects.filter(user = request.user)
        context   = {
               
                     "draft_blog": get_draft,
                     "user_info" : get_user,
                    
                     }
        return render(request,"draft_blog.html",context)
def draft_post(request,id):
       get_blog = get_object_or_404(Blog, id = id)
       get_blog.blog_draft     = False
       get_blog.blog_create_on = get_blog.blog_last_edit
       get_blog.save()
       
       return  redirect("draft")
       
def blog_delete(request,id):
       get_blog = get_object_or_404(Blog, id = id)
       get_blog.delete()
       return redirect("dashbord")

def blog_edit(request,id):
       get_blog           = get_object_or_404(Blog, id = id)
       current_user_value = User_Profile.objects.filter(user = request.user)
       current_blog_value = Blog.objects.filter(id = id)
       category           = Category.objects.all()
       context            = {"current_user" : current_user_value,
                             "current_blog" : current_blog_value,
                             "category"     : category,
                             }       
       if request.method == 'POST' and request.FILES.get("image"):
             category = Category.objects.get(name = request.POST.get("blog_category"))
             title    = request.POST.get("blogtitle")
             content  = request.POST.get("Content")
             img      = request.POST.FILES("image")
             draft    = request.POST.get("checkbox")
             if not category or not title or  not content:
                    messages.warning(request,f'All Fields Are Mendetory      ')
                    return render(request, 'editblog.html', context)
             if draft is None :
                    draft = False
             else: 
                    draft = True

             get_blog.blog_Category = category
             get_blog.blog_title    = title
             get_blog.blog_contant  = content
             get_blog.blog_draft    = draft 
             if  img :
                 fs        = FileSystemStorage()
                 filename  =  fs.save(img.name,img)
                 get_blog.blog_img  = f"uploads/{filename}"
             get_blog.save()
            
             if  draft is False:
               return redirect("dashbord")
             else:
                   return redirect("draft")

       return render(request,'editblog.html',context)



def like(request,post_id):
  current_user  = request.user
  current_blog  = Blog.objects.get( id = post_id)
  liked         = Likes.objects.filter(user_profile = current_user ,blog = current_blog).count()
  current_likes = current_blog.like
  if not liked:
       liked           = Likes.objects.create(user_profile = current_user , blog = current_blog)
       current_likes  += 1
  else:
        liked          = Likes.objects.filter(user_profile = current_user , blog = current_blog).delete()
        current_likes -= 1
  current_blog.like = current_likes
  current_blog.save()
  return redirect("dashbord")           


def viewed_like(request, post_id):
   
    post     = Blog.objects.filter(id = post_id)
    likes  = Likes.objects.filter(blog__id = post_id)
    customer = User_Profile.objects.filter(user = request.user)

    context = {
            "blog_content"  : post, 
            "like"     : likes,
            "customer"      : customer    
              }
   
    return render(request,"show_likes.html",context)

def add_comment(request,post_id):
       blog  = get_object_or_404(Blog,id = post_id)
       user  = User_Profile.objects.get(user = request.user)
      
       if request.method == 'POST':
        comments_texts = request.POST.get("comment_text")
        if comments_texts is None:
              messages.warning(request,f' write comment..')

        else:
              Comment.objects.create(
                    text_comment = comments_texts,
                    post         = blog,
                    commented_by = user,
                   

                              )
              return redirect("viewblog",id = post_id)    
        
       return redirect("viewblog", id=post_id)

def add_reply(request,comment_id):
      comment = get_object_or_404(Comment,id =  comment_id)
      post    = get_object_or_404(Blog   ,id = comment.post.id)
      
      context = {
               "comment": comment,
               "post"    : post,
                }
      return render(request,"addreply.html",context)

def reply(request,comment_id):
      comment = get_object_or_404(Comment , id = comment_id)
      user    = User_Profile.objects.get(user = request.user)
      if request.method == 'POST':
        reply_content = request.POST.get("reply_content")
        if reply_content is None :
              messages.warning(request,f' write....')
        else:
              Comment.objects.create(
                    text_comment = reply_content ,
                    by_Reply     = user,
                    post         = comment.post,
                    parent       = comment
                    
              )
      return redirect("show_reply" , comment_id)

def show_reply(request,comment_id):
      get_comment  = Comment.objects.filter(parent__id=comment_id )
      get_comments = get_object_or_404(Comment, id=comment_id)
      user         = get_object_or_404(User_Profile, user = request.user)
      post         = get_object_or_404(Blog, id = get_comments.post.id)
      

      context     = {
                 "comments" : get_comment,
                 "user"     :  user,
                 "post"     :   post,
                 "parent"   : get_comments
                   }
      return render(request,"showreply.html",context)

def edit_comment(request,comment_id):
      comment     = Comment.objects.filter( id = comment_id)
      context = {
                   "comment": comment
                }
      get_comment = get_object_or_404(Comment,id = comment_id)
      
      print("ram  ................")
      if request.method == 'POST':
            print("hey ram")
            already_comment = request.POST.get("already_comment")
            print(already_comment,"hrerer/....")
            if already_comment is None:
                  print("121212")
                  messages.warning(request,f' write something..')
            else:
                  get_comment.text_comment = already_comment
                
                  get_comment.save()
                  return redirect("show_reply",comment_id)
                  
      
      

      return render(request,"edit_comment.html",context)

def comment_delete(request,comment_id,viewblog_id):
      print(viewblog_id)
      get_comment = get_object_or_404(Comment,id = comment_id)
      get_comment.delete()
      return redirect("viewblog",viewblog_id)