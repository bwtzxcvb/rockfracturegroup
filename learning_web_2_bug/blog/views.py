import redis
from django.conf import settings
from django.db.models import Count
from django.http import StreamingHttpResponse

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT, db=settings.REDIS_DB)


from django.shortcuts import render,get_object_or_404

# Create your views here.
from .models import BlogArticles
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from image.models import Image
from article.models import ArticlePost
from pdfs.models import Pdf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json


def blog_title(request):  
    blogs = BlogArticles.objects.all()    
    return render(request,'blog/titles.html',{'blogs':blogs})

def blog_page(request,blog_id):
    blogs = get_object_or_404(BlogArticles,id=blog_id) 
    pub = blogs.publish
    return render(request,'blog/page.html',{'blog':blogs, 'publish':pub})

@csrf_exempt 
def increaselikes(request):
	if request.method == "POST":
		article_id = request.POST.get("id")
		if article_id:
			try:
				article = ArticlePost.objects.get(id=article_id)
				article.person_likes += 1
				article.save()
				return HttpResponse("success")
			except:
				return HttpResponse("fail")
			
def blog_about(request):
	return render(request,'blog/about.html')	

def blog_archive(request):
	images = Image.objects.all()

	paginator = Paginator(images, 3)
	page = request.GET.get('page')
	try:
		current_page = paginator.page(page)
		images = current_page.object_list
	except PageNotAnInteger:
		current_page = paginator.page(1)
		images = current_page.object_list
	except EmptyPage:
		current_page = paginator.page(paginator.num_pages)
		images = current_page.object_list
	return render(request,'blog/archive.html',{'images':images, "page":current_page})	

def blog_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    pdf = Pdf.objects.get(title=article)
    total_views = r.incr("article:{}:views".format(article.id))
    r.zincrby('article_ranking', 1, article.id)
    
    article_ranking = r.zrange('article_ranking', 0, -1, desc=True)[:20]
    article_ranking_ids = [int(id) for id in article_ranking]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))
    article_rank = most_viewed[0]
    
    article_tags_ids = article.article_tag.values_list("id", flat=True)
    similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags_ids).exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count("article_tag")).order_by('-same_tags', '-created')[:6]
    similar_article = similar_articles[0]
    
    latest_articles = ArticlePost.objects.order_by("-created")[:1]       
        
    return render(request, "blog/content.html",
                  {"article":article,"id" : id,  "slug" : slug, "total_views":total_views, "pdf":pdf, "article_rank":article_rank,"similar_article":similar_article, "latest_articles":latest_articles})

def blog_index(request):
	images = Image.objects.all()
	n = 2
	return render(request, 'index.html', {'images':images,'n':n})
