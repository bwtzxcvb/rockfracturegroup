from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import ContactMessage
from .forms import ContactMessageForm

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse

def contact_page(request):
	message_form = ContactMessageForm()
	return render(request, 'contact/contact.html', {'message_form':message_form})
	
@csrf_exempt
def contact_comment(request):
	if request.method == "POST":
		message_form = ContactMessageForm(data=request.POST)
		if message_form.is_valid():
			new_message = message_form.save(commit=False)                
			new_message.save()
			return HttpResponse("1")
		else:
			return HttpResponse("2")
	else:
		message_form = ContactMessageForm()
    
	return render(request, 'contact/contact.html', {'message_form':message_form})
