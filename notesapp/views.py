from django.shortcuts import render,HttpResponse
from notesapp.models import NotesDb
# Create your views here.
def allnotesshow(request):
  job_request = NotesDb.objects.all()
  context = {'title': job_request}
  return render(request,'index.html',context)
  
def pdfshow(request):
    id = request.GET.get('id')
    context = {'id': id}
    return render(request,'notes.html',context)
  
def page_not_found_view(request, exception):
    return render(request, 'notes.html', status=404)