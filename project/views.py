from django.shortcuts import render
from django.shortcuts import redirect


def home(request):
    return redirect('blog:list')

def blog_list(request):
    return redirect('blog:list')