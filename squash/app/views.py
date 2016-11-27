from django.views import generic
from django.shortcuts import render,redirect

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
            formData = form.cleaned_data
        #     context['result'] = form.get("first_name")
            player=Player(first_name=formData['first_name'],
                last_name=formData['last_name'],
                gender=formData['gender'],
                andrew=formData['andrew'],
                phone=formData['phone'],
                email=formData['email'],
                level=formData['level'],
                frequency=formData['frequency'],
                times=json.dumps(data['times']))
            # player.first_name=data['first_name'][0]
            # player.last_name=data['last_name'][0]
            # player.gender=data['gender'][0]
            # player.andrew=data['andrew'][0]
            # player.phone=data['phone'][0]
            # player.email=data['email'][0]
            # player.level=data['level'][0]
            # player.frequency=data['frequency'][0]
            # player.times=json.dumps(data['times'])

        
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
    # def processForm(data):
    #     if (data.get('times')) is not None:
    #         data.times = repr(data['times'])
    context= {}
    return render(request,'app/filter.html', context)

    
def match_result(request):

    context={'result':None}
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        data = dict(request.POST)

        # create a form instance and populate it with data from the request:
        form = RequirementsForm(request.POST)
        # TODO: might want to copy the data

        # check whether it's valid:
        if form.is_valid():
            formData = form.cleaned_data

        #     context['result'] = form.get("first_name")
            req=Requirements(gender=formData['gender'],
                gender_importance=formData['gender_importance'],
                min_level=formData['min_level'],
                max_level=formData['max_level'],
                level_importance=formData['level_importance'],
                frequency=formData['frequency'],
                frequency_importance=formData['frequency_importance'],
                times=json.dumps(data['times']),
                times_importance=formData['times_importance'])

            # req.gender=formData['gender']
            # req.gender_importance=formData['gender_importance']
            # req.min_level=formData['min_level']
            # req.max_level=formData['max_level']
            # req.level_importance=formData['level_importance']
            # req.frequency=formData['frequency']
            # req.frequency_importance=formData['frequency_importance']

            # req.times=json.dumps(data['times'])
            # req.times_importance=formData['times_importance'][0]



            allPlayers=Player.objects.all()
            partners=req.rankByScore(allPlayers)

            context={
                "partners": partners
            }       
            req.save()
            # context['result'] = data['gender'][0]
            
            return render(request,'app/match_result.html', context)

        else:
            context['result'] = 'error!!!!!'
        # fix this
        return render(request,'app/filter.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        # fix this
        return render(request,'app/filter.html', context)

    # print("A ha")
    # print(dict(request.POST))
    # allPlayers=Player.objects.all()
    # partners=req.rankByScore(allPlayers)

    # context={
    #     "partners": partners
    # }

    # return render(request,'app/match_result.html', context)


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


