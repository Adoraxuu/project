from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm
from .models import Post, Comment
from taggit.models import Tag

def list(request, tag_slug=None):
    if tag_slug:
        tag = Tag.objects.filter(slug=tag_slug).first()
        posts = Post.objects.filter(tags__in=[tag]) #只要包含我們搜尋的tag就列出來
    else:
        posts = Post.objects.all()
    tag_list = Tag.objects.all()
    paginator = Paginator(posts,3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'blog/list.html',
        {'posts': posts, 'tag_list': tag_list}
    )

def detail(request, year, month, day, slug):
    post = Post.objects.filter(
        published_date__year=year,
        published_date__month=month,
        published_date__day=day,
        slug=slug,
    ).first()
    comments = post.comments.filter(active=True) 
    new_comment = None
    if request.method == 'POST': 
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid(): 
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        'blog/detail.html',
        {'post': post,
         'comments': comments,
         'new_comment': new_comment,
         'comment_form': comment_form
         }
    )

def author(request):
    return render(request, 'blog/author.html')

def testing(request):
  template = loader.get_template('blog/testing.html')
  return HttpResponse(template.render()) 

