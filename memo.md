會自動生成多個檔案和資料夾
## settimgs.py
此app的配置，包含資料庫

# urls.py
url映射

```python
urlpatterns = [
    path('admin/', admin.site.urls),
]
```
默認admin是預設的

## wsgi
生成符合wsgi標準的app


## app
整個網站分很多模塊，可以把不同模塊整理出來，稱為app
像是blog app，可以運用指令生成：
```python
$ python manage.py startapp blog
```
### apps.py
進行相關的配置，像是裡面默認：
```python
class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
```

### models.py
數據庫表格

### test.py
測試

### view.py
類似於Ruby的controller，能夠在這裡請求外部內容

## 想使用mysql當作我們的數據庫
之後再去看
---

## 設計Table
```python
# project/blog/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):

    STATS_OPTIONS = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts', 
        )
    
    body = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=STATS_OPTIONS,
        default='draft')
    
    class Meta:
        ordering = ('-published_date',)

    def __str__(self):
        return self.title
```
`from django.db import models`
從blog model裡面創建叫post的classes，從djangoDB繼承

`slug = models.Slug.Field(max_length=250,unique_for_date='publish')`
slug = 通過id標示他 or 通過文章標題標示（就是slug）

因為django會默認幫忙設置user的表，所以可以使用Foreign_key去設置

`on_delete=models.CASCADE,`
與user關聯的文章也一併刪除

```python
class Meta:
    ordering = ('-publish')
```
降序，最新放最上面

數據庫設計好後，要和setting說，我們有一個blog的app，我們blog需要在數據庫進行初始化
`project/project/settings.py`
在裡面添加
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
]
```
添加完成之後就可以運行migrations
```python
  blog/migrations/0001_initial.py
    - Create model Post
```
`$ python manage.py makemigrations blog`
blog/migrations資料夾生成`0001_initial.py`文件，

可以下命令看他執行的sql語法
`$ python manage.py sqlmigrate blog 0001`

```sql
BEGIN;
--
-- Create model Post
--
CREATE TABLE "blog_post" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(200) NOT NULL, "body" text NOT NULL, "published_date" datetime NOT NULL, "created_date" datetime NOT NULL, "updated_date" datetime NOT NULL, "status" varchar(10) NOT NULL, "author_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "blog_post_author_id_dd7a8485" ON "blog_post" ("author_id");
COMMIT;
```
可以看到他新增了一張名稱為`blog_post`的Table
最後可以透過以下指令去執行
`$ python manage.py migrate`

---

## admin站點使用

這是Python內建的功能，可以從db.sqlite3裡面的Table就可以看得出來，有像是permission, admin等等的Table，當我們`python manage.py runserver`時，瀏覽器開啟`http://127.0.0.1:8000/admin`就能夠看到登入介面。

不過需要先創建username & password，可以使用以下指令創建：
`$ python manage.py createsuperuser`

## 把post加進去admin裡
blog/admin.py
`from .models import post`

也可以透過admin新增資料

## 改變post顯示的項目

```python
#project/blog/admin.py
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
```
![](pic/admin-post-table.png "post-table")

## 添加新欄位
```
#/Users/adora/Python/my_project/project/blog/models.py
slug = models.SlugField(max_length=200, unique=True, blank=True)
```
```pthon
$ python manage.py makemigrations blog      
```
```terminal   
Migrations for 'blog':
  blog/migrations/0002_post_slug.py
    - Add field slug to post
```
```
$ python manage.py migrate
```
```
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, blog, contenttypes, sessions
Running migrations:
  Applying blog.0002_post_slug... OK
```

## 客製化

```python
# project/blog/admin.py
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','author', 'published_date')
    list_filter = ('author', 'published_date')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
```
![](pic/admin.png)

關於更多客製化，可以參考：[django docs](https://docs.djangoproject.com/en/5.0/ref/contrib/admin/)

## 使用ORM

$ cd/python
$ python manage.py shell

```python
$ python manage.py shell
(InteractiveConsole)
>>> from blog.models import Post
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='admin')
>>> user
<User: admin>
>>> post = Post(title='created from shell', slug='create-from-shell', body='this is body', author=user,status='draft')
>>> post
<Post: created from shell>
post.save()
```
更新
```python
>>> post.title = 'new title'
>>> post.title
'new title'
>>> post.save()
```




## 使用ORM

$ cd/python
$ python manage.py shell

```python
$ python manage.py shell
(InteractiveConsole)
>>> from blog.models import Post
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='admin')
>>> user
<User: admin>
>>> post = Post(title='created from shell', slug='create-from-shell', body='this is body', author=user,status='draft')
>>> post
<Post: created from shell>
post.save()
```
更新
```python
>>> post.title = 'new title'
>>> post.title
'new title'
>>> post.save()
```


## ORM指令
```python
$ python manage.py shell

Python 3.12.2 (main, Feb  6 2024, 20:19:44) [Clang 15.0.0 (clang-1500.1.0.2.5)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)

>>> from blog.models import Post
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='admin')
>>> user
<User: admin>
>>> post = Post(title='created from shell', slug='create-from-shell', body='this is body', author=user,status='draft')
>>> post
<Post: created from shell>
>>> post.save()
>>> post.title
'created from shell'
>>> post.title = ('new title')
>>> post.title.save()
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: 'str' object has no attribute 'save'
>>> psot.save()
Traceback (most recent call last):
  File "<console>", line 1, in <module>
NameError: name 'psot' is not defined
>>> post.title = 'new title'
>>> post.title
'new title'
>>> post.save()
```
### get
```
>>> >>> post = Post.objects.get(title = 'new title')
>>> post
<Post: new title>
```

### filter
```
>>> psot = Post.objects.filter(title='new title')
>>> post
<Post: new title>
```

### all
```
post = Post.objects.all()
>>> post
<QuerySet [<Post: new title>, <Post: hello world>]>
```

```
>>> for p in post:
...     print(p)
... 
new title
hello world
```

### first
```
>>> post = Post.objects.all().first()
>>> post
<Post: new title>
```
### order_by
```
>>> post = Post.objects.order_by('title')
>>> post
<QuerySet [<Post: hello world>, <Post: new title>]>
>>> post = Post.objects.order_by('-title')
>>> post
<QuerySet [<Post: new title>, <Post: hello world>]>
```

## 刪除
```
>>> delete = post.filter(title='hello world')
>>> delete.delete()
(1, {'blog.Post': 1})
>>> post = post.filter(title='hello world')
>>> 
```

## 建立前台view
先到主層的資料夾去設定url
```python
#project/project/urls.py
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog',include('blog.urls', namespace= 'blog')),#新增這行
]
```
## templates語言
類似Jinja2
linebreaks: string 裡面有換行就換行
empty: for 如果是空的就顯示...
