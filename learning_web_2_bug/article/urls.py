from django.urls import path
from .import views, list_views

app_name = "article"

urlpatterns = [
        path('article-column/',views.article_column, name="article_column"),
        path('rename-column/',views.rename_article_column, name="rename_article_column"),
        path('del-column/',views.del_article_column,name="del_article_column"),
        path('article-post/',views.article_post,name="article_post"),
        path('article-list/',views.article_list,name="article_list"),
        path('article-detail/<int:id>/<slug:slug>',views.article_detail,name="article_detail"),
        path('del-article',views.del_article,name="del_article"),
        path('redit-article/<int:article_id>/', views.redit_article, name="redit_article"),
        path('list-article-titles/', list_views.article_titles, name="article_titles"),
        path('article-content/<int:id>/<slug:slug>', list_views.article_detail, name="article_content"),
        path('list-article-titles/<username>/', list_views.article_titles, name="author_articles"),
        path('like-article/', list_views.like_article, name="like_article"),
        path('article-content/<int:id>/<slug:slug>/<int:get_nodeid>', list_views.re_comment, name="re_comment"),
        path('article-tag/', views.article_tag, name="article_tag"),
        path('del-article-tag/', views.del_article_tag, name="del_article_tag"),
        path('download_1/', list_views.download_1, name = "download_1"),
        path('search.html',views.MySearchView(), name='haystack'),
        path('download_2/', list_views.download_2, name = "download_2"),
        path('download_3/', list_views.download_3, name = "download_3"), 
        path('download_4/', list_views.download_4, name = "download_4"), 
        path('download_5/', list_views.download_5, name = "download_5"),                       
]

#urlpatterns = [
        #path('list-article-titles/', list_views.article_titles, name="article_titles"),
        #path('article-content/<int:id>/<slug:slug>', list_views.article_detail, name="article_content"),
#] #path('article-comment/', list_views.article_comment, name="article_comment"),
