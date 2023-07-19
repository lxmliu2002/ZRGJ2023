from django.shortcuts import render,redirect
from python_hint.settings import graph
from py2neo import Node,Relationship,NodeMatcher
from django.http import HttpResponse
import json
import numpy as np


# Create your views here.

def codes(request):
    return render(request,'python_code/index.html')

def query(request):
    return render(request,'python_code/query.html')

def getType(request):
    line = request.GET.get('line')
    return HttpResponse(json.dumps({'type':line}))
