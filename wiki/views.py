from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.
def wiki_index(request):
    return render(request, 'index.html')

def testing(request):
  template = loader.get_template('testing.html')
  return HttpResponse(template.render()) 

