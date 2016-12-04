## django的网站搭建
**参考：**[官方文档](https://docs.djangoproject.com/en/1.10/intro/)
*注意:* 操作均在virtualenv中进行，虚拟目录为web-share/
- 创建项目 at `web-share/`
  - django-admin startproject mysite
- 创建app `web-share/mysite/`
  - python manage.py startapp writefile
- 合并模块，使django能搜索到 writefile 下的目录 ` `web-share/mysite/``
  - vi writefile/model.py
随意建立一个类
```
class Fuck(models.Model):
       a=1
```
  - `vi mysite/settings.py`
添加
```
INSTALLED_APPS = [
'writefile.apps.WritefileConfig',
]
```
  - 创建模块，migrate后django就可以搜索writefile中的templates目录
```
python manage.py makemigrations
python manage.py migrate
```

- url 设置 at `web-share/mysite/`
  - 在 writefile 中新建文件 urls.py
输入内容
```
from django.conf.urls import url 
from . import views
urlpatterns =[
       url(r'^$', views.getmsg, name='getmsg'),
]
```
url()的正则匹配：不会匹配域名和表单，在上面的作用是域名后不加任何字符，就调用getmsg函数
  - 为了能使django找到writefile中的urls文件，需要在mysite/urls.py中添加
```
from django.conf.urls import url, include
urlpatterns = [
url(r'^$', include('writefile.urls')),
]
```
**django查找urls的流程：**
-> mysite/mysite/urls.py ->(通过include) mysite/writefile/urls.py->(正则匹配) 调用writefile/views.py中的函数

* 使用html文件作为显示 at `mysite/writefile/`
新建templates/writefile/目录，在其中放置html文件
  - views.py 设置 at `web-share/mysite/writefile/`
添加`from django.template import loader` 用于导入html，views.py中的getmsg函数
```
def getmsg(request):
    template = loader.get_template("writefile/index.html")
    ....
    return HttpResponse(template.render(cont, request))
```
cont为与html中变量有关的字典

## 将adjango项目部署到nginx+uwsgi
按照[ubuntu中web服务器配置nginx+uwsgi+django](http://www.jianshu.com/p/0988624ff307)中步骤进行，不同的是，方便起见，将django的端口设置为默认端口，这与nginx中的默认端口冲突，因此需要将`/etc/nginx/sites-available/default`的80端口改成其它的
**mysite_nginx.conf 文件**
```
# the upstream component nginx needs to connect to
upstream django {
    server unix:/home/zooo/web-share/mysite/mysite.sock; # for a file socket
    #server 127.0.0.1:8001; # for a web port socket (we'll use this first)
}

# configuration of the server
server {
    # the port your site will be served on
    listen      80;
    # the domain name it will serve for
    server_name localhost; # substitute your machine's IP address or FQDN
    charset     utf-8;

    # max upload size
    client_max_body_size 75M;   # adjust to taste

    # Django media
    location /media  {
        alias /home/zooo/web-share/mysite/media; 
        autoindex on;
    }

    location /static {
        alias /home/zooo/web-share/mysite/static;
    }

    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     /home/zooo/web-share/mysite/uwsgi_params;
    }
}
```
**mysite_uwsgi.ini文件**
```
# mysite_uwsgi.ini file
[uwsgi]

# Django-related settings
# the base directory (full path)
chdir           = /home/zooo/web-share/mysite
# Django's wsgi file
module          = mysite.wsgi
# the virtualenv (full path)
home            = /home/zooo/web-share/

# process-related settings
# master
master          = true
# maximum number of worker processes
processes       = 4
# the socket (use the full path to be safe
socket          = /home/zooo/web-share/mysite/mysite.sock
# ... with appropriate permissions - may be needed
chmod-socket    = 666
```
