from django.shortcuts import render

from django.http import Http404
from django.http import HttpResponseRedirect

from .forms import NameForm

from .models import Player

# Create your views here.

def index(request):
    players=Player.objects.all()
    context = {}
    context['greetings'] = "Hi! My name is"
    context['name'] = "Flora"
    return render(request, 'app/index.html', context)

def partner(request):
    context={}
    
    return render(request,'app/partner.html', context)

def signup(request):
    context={'result':None}
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        data = dict(request.POST)
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
        #     context['result'] = form.get("first_name")
            context['result'] = data['first_name'][0]
        else:
            context['result'] = 'error!!!!!'
        return render(request,'app/signup.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        return render(request,'app/signup.html', context)

def profile(request,user_id):
    player=Player.objects.get(pk=user_id)
    context={

        'player': player,
    }

    try: 
        player=Player.objects.get(pk=user_id)
    except Player.DoesNotExist:
        raise Http404("Player does not exist")
    return render (request, 'app/profile.html',context)



