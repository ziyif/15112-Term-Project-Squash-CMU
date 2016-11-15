from django.shortcuts import render

# Create your views here.

def index(request):
    context = {}
    context['greetings'] = "Hi! My name is"
    context['name'] = "Flora"
    return render(request, 'app/index.html', context)
