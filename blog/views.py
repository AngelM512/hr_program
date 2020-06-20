from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
from blog.models import Post
# Create your views here.
today = date.today()
day_format = today.strftime("%B %d, %Y")


def home(request):
    context = {
        'posts' : Post.objects.all()
    }

    response = "blog/home.html"
    return render(request, response, context)

def about(request):
    response = "blog/about.html"
    return render(request, response, {'title':'Blog'})

def contact_us(request):
    response = "blog/contact.html"
    return render(request, response, {'title':'Contact'})
