from django.shortcuts import render, render_to_response
from django.shortcuts import HttpResponse
# Create your views here.

def index(request):
    #request.POST
    #request GET
    #return HttpResponse("Hello world inside index()!")
    #return render(request, "story.html")
    return render(request, "index.html")
    #return render_to_response("index.html", dict(entries=entries),context_instance=RequestContext(request)))