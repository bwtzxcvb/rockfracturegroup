from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import PdfForm
from .models import Pdf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from article.models import ArticlePost

@login_required(login_url='/account/login/')
@csrf_exempt
def upload_pdf(request):
	if request.method == "POST":
		form = PdfForm(data=request.POST)
		if form.is_valid():
			try:
				new_item = form.save(commit=False)
				new_item.title = ArticlePost.objects.get(id=request.POST['pdf_articleid'])
				new_item.user = request.user
				new_item.save()
				return JsonResponse({'status':"0"})
			except:
				return JsonResponse({'status':"1"})
		else:
			return JsonResponse({'status':"2"})		
	else:
		article_titles = request.user.article.all()
		pdf_post_form = PdfForm()
		return render(request, 'pdf/pdf_post.html', {'article_titles':article_titles, 'pdf_post_form':pdf_post_form})

@login_required(login_url="/account/login")
def list_pdfs(request):
	pdfs = Pdf.objects.filter(user=request.user)
	paginator = Paginator(pdfs, 2)
	page = request.GET.get('page')
	try:
		current_page = paginator.page(page)
		pdfs = current_page.object_list
	except PageNotAnInteger:
		current_page = paginator.page(1)
		pdfs = current_page.object_list
	except EmptyPage:
		current_page = paginator.page(paginator.num_pages)
		pdfs = current_page.object_list
	return render(request, 'pdf/list_pdfs.html', {"pdfs":pdfs, "page":current_page})



@login_required(login_url="/account/login")
@require_POST
@csrf_exempt
def del_pdf(request):
	pdf_id = request.POST['pdf_id']
	try:
		pdf = Pdf.objects.get(id=pdf_id)
		pdf.delete()
		return JsonResponse({'status':"1"})
	except:
		return JsonResponse({'status':"2"})
