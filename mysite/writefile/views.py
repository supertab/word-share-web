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
    template = loader.get_template("writefile/index.html")
    f = open('./data.txt', 'r')
    getname = ''
    history = ''
    # read the end line at file
    if len(f.read()):
        f.seek(0)
        history = list(f)[-1]
    if 'your_name' in request.POST:
        getname = request.POST['your_name'] 
    cont = {'getname': getname,
            'history': history,
            }
    f.close()
    f = open('./data.txt', 'a')
    if len(getname):
        f.write(getname+'\n')
    f.close()
    return HttpResponse(template.render(cont, request))
