from django.contrib import admin
from django.urls import path
from blog import views

app_name = "blog"

urlpatterns = [
    path('',views.blog_title,name='blog_title'),
    path('<int:blog_id>/',views.blog_page,name='blog_page'),
    path('increase-likes/', views.increaselikes, name='increase_likes'),
    path('about/',views.blog_about, name='blog_about'),
    path('archive/',views.blog_archive, name='blog_archive'),
    path('archive-detail/<int:id>/<slug:slug>',views.blog_detail, name='blog_detail'),
]
