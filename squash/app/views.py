from django.views import generic
from django.shortcuts import render

from django.http import Http404
from django.http import HttpResponseRedirect

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import NameForm, RequirementsForm

from .models import Player,Requirements
import json


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

# http://stackoverflow.com/questions/1110153/what-is-the-most-efficent-way-to-store-a-list-in-the-django-models
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
            player=Player()
            player.first_name=data['first_name'][0]
            player.last_name=data['last_name'][0]
            player.gender=data['gender'][0]
            player.andrew=data['andrew'][0]
            player.phone=data['phone'][0]
            player.email=data['email'][0]
            player.level=data['level'][0]
            player.frequency=data['frequency'][0]
            player.times=json.dumps(data['times'])

        
            player.save()
            user_id=player.id
            context['result'] = data['first_name'][0]
            return render(request,'app/profile.html', context)

        else:
            context['result'] = 'error!!!!!'
        return render(request,'app/signup.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        return render(request,'app/signup.html', context)

def filter(request):
    context={'result':None}
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        data = dict(request.POST)
        # create a form instance and populate it with data from the request:
        form = RequirementsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
        #     context['result'] = form.get("first_name")
            req=Requirements()
       
            req.gender=data['gender'][0]
            req.gender_importance=data['gender_importance'][0]
            req.min_level=data['min_level'][0]
            req.max_level=data['max_level'][0]
            req.level_importance=data['level_importance'][0]
            req.frequency=data['frequency'][0]
            req.frequency_importance=data['frequency_importance'][0]
            req.times=json.dumps(data['times'])
            req.times_importance=data['times_importance'][0]
        
            req.save()
            context['result'] = data['gender'][0]
            return render(request,'app/filter.html', context)

        else:
            context['result'] = 'error!!!!!'
        return render(request,'app/filter.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        return render(request,'app/filter.html', context)




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

class PlayerCreate(CreateView):
    model=Player
    fields=['andrew','first_name','last_name','gender']


