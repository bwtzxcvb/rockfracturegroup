from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import NewsColumn, NewsPost, NewsTag
from django.views.decorators.csrf import csrf_exempt
from .forms import NewsColumnForm, NewsPostForm, NewsTagForm
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
import json

@login_required(login_url='/account/login')
@csrf_exempt
def news_column(request):
    if request.method == "GET":
        columns = NewsColumn.objects.filter(user=request.user)
        column_form = NewsColumnForm()
        return render(request,"news/column/news_column.html",{"columns":columns, "column_form":column_form})
    
    if request.method == "POST":
        column_name = request.POST['column']
        columns = NewsColumn.objects.filter(user_id=request.user.id, column=column_name)
        
        if columns:
            return HttpResponse("2")
        else:
            NewsColumn.objects.create(user=request.user,column=column_name)
            return HttpResponse("1")

@login_required(login_url='account/login')
@require_POST
@csrf_exempt
def rename_news_column(request):
    column_name = request.POST["column_name"]
    column_id = request.POST["column_id"]
    
    try:
        line = NewsColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")

@login_required(login_url='account/login')
@require_POST
@csrf_exempt
def del_news_column(request):
    column_id = request.POST["column_id"]
    try:
        line = NewsColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")
        
@login_required(login_url="/account/login")
@csrf_exempt
def news_post(request):
    if request.method == "POST":
        news_post_form = NewsPostForm(data=request.POST)
        if news_post_form.is_valid():
            cd = news_post_form.cleaned_data
            try:
                new_news = news_post_form.save(commit=False)
                new_news.user = request.user
                new_news.column = request.user.news_column.get(id=request.POST['column_id'])
                new_news.save()
                tags = request.POST['tags']
                if tags:
                    for atag in json.loads(tags):
                        tag = request.user.news_alltag.get(tag=atag)
                        new_news.news_tag.add(tag)
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        news_post_form = NewsPostForm()
        news_columns = request.user.news_column.all()
        news_tags = request.user.news_alltag.all()
        return render(request,"news/column/news_post.html",
                        {"news_post_form":news_post_form,
                        "news_columns":news_columns,
                        "news_tags":news_tags})

@login_required(login_url='/account/login/')
def news_list(request):
    news_list = NewsPost.objects.filter(user=request.user)
    paginator = Paginator(news_list, 2)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        news = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        news = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        news = current_page.object_list
    return render(request,"news/column/news_list.html",{"news":news, "page":current_page})

@login_required(login_url='/account/login/')
def news_detail(request, id, slug):
    news = get_object_or_404(NewsPost, id=id, slug=slug)
    news_tags_ids = news.news_alltag.values_list("id", flat=True)
    similar_news = NewsPost.objects.filter(news_tags__in=news_tags_ids).exclude(id=news.id)
    similar_news = similar_news.annotate(same_tags=Count("news_tags")).order_by('-same_tags', '-created')[:4]
    return render(request, "article/column/article_detail.html",{"article":article})

@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_news(request):
    new_id = request.POST['new_id']
    try:
        news =NewsPost.objects.get(id=new_id)
        news.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")
        
        
@login_required(login_url='/account/login')
@csrf_exempt
def redit_news(request,news_id):
    if request.method == "GET":
        news_columns = request.user.news_column.all()
        news = NewsPost.objects.get(id=news_id)
        this_news_form = NewsPostForm(initial={"title":news.title})
        this_news_column = news.column
        this_news_tags = news.news_tag

        return render(request,"news/column/redit_news.html",
            {"news":news,
             "news_columns":news_columns,
             "this_news_column":this_news_column,
             "this_news_form":this_news_form,
             "this_news_tags":this_news_tags})
    else:
        redit_news = NewsPost.objects.get(id=news_id)
        try:
            redit_news.column = request.user.news_column.get(
                                                        id=request.POST['column_id'])
            redit_news.title = request.POST['title']
            redit_news.body = request.POST['body']
            redit_news.save()
            return HttpResponse("1")
        except:
            return HttpResponse("2")

@login_required(login_url='/account/login')
@csrf_exempt
def news_tag(request):
    if request.method == "GET":
        news_tags = NewsTag.objects.filter(user=request.user)
        news_tag_form = NewsTagForm()
        return render(request, "news/tag/tag_list.html",
                      {"news_tags":news_tags,
                       "news_tag_form":news_tag_form})
                       
    if request.method == "POST":
        tag_post_form = NewsTagForm(data=request.POST)
        if tag_post_form.is_valid():
            try:
                new_tag = tag_post_form.save(commit=False)
                new_tag.user = request.user
                new_tag.save()
                return HttpResponse("1")
            except:
                return HttpResponse("the data cannot save.")
        else:
            return HttpResponse("sorry,the form is not valid.")

@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def del_news_tag(request):
    tag_id = request.POST['tag_id']
    try:
        tag = NewsTag.objects.get(id=tag_id)
        tag.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

