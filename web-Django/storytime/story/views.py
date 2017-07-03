from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.

def index(request):
    #request.POST
    #request GET
    return HttpResponse("Hello world inside index()!")