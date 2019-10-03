from django.urls import path
from .import views

app_name = "news"

urlpatterns = [
        path('news-column/',views.news_column, name="news_column"),
        path('rename-news-column/',views.rename_news_column, name="rename_news_column"),
        path('del-news-column/',views.del_news_column,name="del_news_column"),
        path('news-post/',views.news_post,name="news_post"),
        path('news-list/',views.news_list,name="news_list"),
        path('news-detail/<int:id>/<slug:slug>',views.news_detail,name="news_detail"),
		path('del-news',views.del_news,name="del_news"),
		path('redit-news/<int:news_id>/', views.redit_news, name="redit_news"),
		path('news-tag/', views.news_tag, name="news_tags"),
		path('del-news-tag/', views.del_news_tag, name="del_news_tags"),        
]
