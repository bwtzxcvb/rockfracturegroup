import redis
from django.conf import settings
from django.db.models import Count
from django.http import StreamingHttpResponse

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT, db=settings.REDIS_DB)


from django.shortcuts import render, get_object_or_404
# Create your views here.
from .models import ArticleColumn, ArticlePost, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import CommentForm

def article_titles(request,username=None):
    if username:
        user = User.objects.get(username=username)
        articles_title = ArticlePost.objects.filter(author=user)
        try:
            userinfo = user.userinfo
        except:
            userinfo = None
    else:
        articles_title =ArticlePost.objects.all()
        
    paginator = Paginator(articles_title, 2)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list

    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list

    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
        
    if username:
        return render(request,"article/list/author_articles.html",
                {"articles":articles, "page":current_page,
                 "userinfo":userinfo, "user":user})
    else:
        return render(request,"article/list/article_titles.html",{"articles":articles, "page":current_page})

@csrf_exempt
@login_required()
def article_detail(request, id, slug, parent_comment_id=None):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    total_views = r.incr("article:{}:views".format(article.id))
    r.zincrby('article_ranking', 1, article.id)
    
    article_ranking = r.zrange('article_ranking', 0, -1, desc=True)[:10]
    article_ranking_ids = [int(id) for id in article_ranking]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))
    
    article_tags_ids = article.article_tag.values_list("id", flat=True)
    similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags_ids).exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count("article_tag")).order_by('-same_tags', '-created')[:4]
    
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article #watch out!
            new_comment.commentator = request.user
            
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                new_comment.parent_id = parent_comment.get_root().id
                new_comment.reply_to = parent_comment.commentator
                new_comment.save()
                return HttpResponse('5')
                
            new_comment.save()
            return HttpResponse("5")
        else:
            return HttpResponse("6")
    else:
        comment_form = CommentForm()
    comments_list = article.comments.all()
    paginator = Paginator(comments_list, 6)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        comments = current_page.object_list

    except PageNotAnInteger:
        current_page = paginator.page(1)
        comments = current_page.object_list

    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        comments = current_page.object_list
        
    return render(request, "article/list/article_content.html",
                  {"article":article, "total_views":total_views, 
                  "most_viewed":most_viewed, 'comment_form':comment_form, 
                  'comments': comments, 'page' : current_page, 
                  "comments_list" : comments_list,
                  "id" : id,  "slug" : slug, 
                  "parent_comment_id" : parent_comment_id,
                  "similar_articles":similar_articles})




@require_POST
@csrf_exempt
@login_required()
def like_article(request):
    article_id = request.POST.get("id")
    action = request.POST.get("action")
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action == "like":
                article.users_like.add(request.user)
                return HttpResponse("1")
            else:
                article.users_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("3")

@csrf_exempt

def re_comment(request, id, slug, get_nodeid):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    id = id
    slug = slug
    get_nodeid = get_nodeid
    parent_comment_id = get_nodeid
    
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article #watch out!
            new_comment.commentator = request.user
            
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                new_comment.parent_id = parent_comment.get_root().id
                new_comment.reply_to = parent_comment.commentator
                new_comment.save()
                return HttpResponse('5')
                
            new_comment.save()
            return HttpResponse("6")
        else:
            return HttpResponse("7")
    else:
        comment_form = CommentForm()
    
    return render(request,'article/list/reply_content.html',{'comment_form':comment_form,'id':id , 'slug':slug, 'get_nodeid':get_nodeid})



def download_1(request):
    file_name = 'static/downfiles/fracture_generator.rar'
    def read_file(file_name,chunk_size=512):
        with open(file_name,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    
    the_file_name = 'fracture_generator.rar'
    response = StreamingHttpResponse(read_file(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response

def download_2(request):
    file_name = 'static/downfiles/fracture_grouping.rar'
    def read_file(file_name,chunk_size=512):
        with open(file_name,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    
    the_file_name = 'fracture_grouping.rar'
    response = StreamingHttpResponse(read_file(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response

def download_3(request):
    file_name = 'static/downfiles/general_block.rar'
    def read_file(file_name,chunk_size=512):
        with open(file_name,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    
    the_file_name = 'general_block.rar'
    response = StreamingHttpResponse(read_file(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response

def download_4(request):
    file_name = 'static/downfiles/joint_oky.rar'
    def read_file(file_name,chunk_size=512):
        with open(file_name,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    
    the_file_name = 'joint_oky.rar'
    response = StreamingHttpResponse(read_file(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response

def download_5(request):
    file_name = 'static/downfiles/slope_block.rar'
    def read_file(file_name,chunk_size=512):
        with open(file_name,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    
    the_file_name = 'slope_block.rar'
    response = StreamingHttpResponse(read_file(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response
