from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageForm, ImagePostForm
from .models import Image
from article.models import ArticlePost
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required(login_url='/account/login/')
@csrf_exempt
def upload_image(request):
	if request.method == "POST":
		form = ImageForm(data=request.POST)
		if form.is_valid():
			try:
				new_item = form.save(commit=False)
				new_item.title=ArticlePost.objects.get(id=request.POST['image_articleid'])
				new_item.user = request.user
				new_item.save()
				return JsonResponse({'status':'0'})
			except:
				return JsonResponse({'status':"1"})			
		else:
			return JsonResponse({'status':"2"})
			
	else:
		article_titles = request.user.article.all()		
		image_post_form = ImageForm()
		return render(request,'image/image_post.html', {'article_titles':article_titles, 'image_post_form':image_post_form})

@login_required(login_url="/account/login")
def list_images(request):
	images = Image.objects.filter(user=request.user)
	paginator = Paginator(images, 2)
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
	return render(request, 'image/list_images.html', {"images":images, "page":current_page})



@login_required(login_url="/account/login")
@require_POST
@csrf_exempt
def del_image(request):
	image_id = request.POST['image_id']
	try:
		image = Image.objects.get(id=image_id)
		image.delete()
		return JsonResponse({'status':"1"})
	except:
		return JsonResponse({'status':"2"})
