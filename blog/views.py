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
    # List of active comments for this post
    comments = post.comments.filter(active=True) #過濾出所有active的comment
    new_comment = None
    if request.method == 'POST': #submit就是發送post請求
        # A comment was posted
        comment_form = CommentForm(data=request.POST) # 讀取form數據，產生comment_form對象
        if comment_form.is_valid(): #驗證是否正確
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False) #新建一個new_comment對象，但不save
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm() #如果不是post 是get，就做一個form的顯示

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

