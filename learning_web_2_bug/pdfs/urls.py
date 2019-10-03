from django.urls import path
from . import views

app_name = "pdf"

urlpatterns = [
	path("list-pdfs/", views.list_pdfs, name="list_pdfs"),
	path("upload-pdf/", views.upload_pdf, name='upload_pdf'),
	path('del-pdf/', views.del_pdf, name='del_pdf'),
]
