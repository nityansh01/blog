from django. urls import path
from django.conf import settings
from .import views 
from django.conf.urls.static import static


urlpatterns =[
        
    path("",views.home,name="home"),
    path("signup/",views.signup,name="signup"),
    path("signin/",views.signin,name="signin"),
    path("signout/",views.signout,name="signout"),
    path("dashbord/",views.dashbord,name="dashbord"),
    path('add_category/',views.add_category,name="add_category"),
    path("Write_Blog/",views.Write_Blog,name='Write_Blog'),
    path("userprofile/",views.userprofile,name='userprofile'),
    path ("draft/",views.draft_show,name='draft'),
   
    
   
   



    
#dynamic Url 
  
   path("viewblog/<int:id>",views.viewblog,name='viewblog'),
   path("editprofile/<int:id>,",views.editprofile,name='editprofile'),
   path("changepassword/<int:id>",views.changepassword,name='changepassword'),
   path("yourblog/<int:user_id>",views.yourblog,name='yourblog'),
   path("draft_post/<int:id>",views.draft_post,name='draftpost'),
   path("blog_delete/<int:id>",views.blog_delete,name='deleteblog'),
   path("blog_edit/<int:id>",views.blog_edit,name='editblog'),
   path("like/<int:post_id>",views.like,name="like"),
   path("viewed_like/<int:post_id>",views.viewed_like,name='viewed_like'),
   path("add_comment/<int:post_id>",views.add_comment,name='add_comment'),
   path("add_reply/<int:comment_id>",views.add_reply ,name='add_reply'),
   path("reply/<int:comment_id>",views.reply,name = 'reply'),
   path("show_reply/<int:comment_id>",views.show_reply,name='show_reply'),
   path("edit_comment/<int:comment_id>",views.edit_comment,name='edit_comment'),
   path("comment_delete/<int:comment_id>/<int:viewblog_id>",views.comment_delete,name='comment_delete'),
   



] 
