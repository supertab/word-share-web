from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.

import re

def index(request):
    template = loader.get_template('writefile/index.html')
    cont = {'number':2}
    return HttpResponse(template.render(cont, request))

def getmsg(request):
    #逻辑：当提交后在history显示提交的数据
    template = loader.get_template("writefile/index.html")
    getname = ''
    history = ''
    if 'your_name' in request.POST:
        getname = request.POST['your_name'] 

    # write message into file
    if len(getname):
        f = open('./data.txt', 'a')
        f.write(getname+'\n')
        f.close()

    # read the end line at file
    f = open('./data.txt', 'r')
    if len(f.read()):
        f.seek(0)
        history = list(f)[-1]
    f.close()
    cont = {'getname': getname,
            'history': history,
            }

    return HttpResponse(template.render(cont, request))
