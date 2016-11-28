from django.views import generic
from django.views.generic import View, DetailView
from django.shortcuts import render,redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponseRedirect


from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import NameForm, RequirementsForm,UserForm

from .models import Player,Requirements
import json


# Create your views here.

def index(request):
    context={}
    players=Player.objects.all()

    if request.user.is_authenticated():
        try:

            context = {'player_id' : request.user.player.pk,
                        'login_status':request.user.username}
        except:
            context={}
    context['greetings'] = "Hi! "
    context['instructions'] = "Please log in to enjoy all features."
    return render(request, 'app/index.html', context)

def partner(request):
    context={}
    if request.user.is_authenticated():
        try:

            context = {'player_id' : request.user.player.pk,
                        'login_status':request.user.username}
        except:
            context={}
    # context={'player_id': request.user.player.pk}

    return render(request,'app/partner.html', context)

# http://stackoverflow.com/questions/1110153/what-is-the-most-efficent-way-to-store-a-list-in-the-django-models
def signup(request):
    context={'result':""}
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        data = dict(request.POST)
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            formData = form.cleaned_data
        #     context['result'] = form.get("first_name")
            user=request.user
            user.player=Player(user=request.user,
                first_name=formData['first_name'],
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

            user.player.save()
            
            context['result'] = data['first_name'][0]
            return redirect('/user/{}'.format(user.player.pk))
            # return render(request,'app/profile.html', context)

        else:
            context['result'] = 'Plase make sure you fill in the form correctly.'
        return render(request,'app/signup.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        return render(request,'app/signup.html', context)

def updateProfile(request):
    context={}
    if request.user.is_authenticated():
        try:

            context = {'player_id' : request.user.player.pk,
                        'login_status':request.user.username}
        except:
            context={}

    # context={'player_id':request.user.player.id}
    if request.method == 'POST':
        data = dict(request.POST)
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            formData = form.cleaned_data
        #     context['result'] = form.get("first_name")
            user=request.user
            user.player.delete()
            player=Player(user=request.user,
                first_name=formData['first_name'],
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
            
            context['result'] = data['first_name'][0]
            
            return redirect('/user/{}'.format(user.player.pk))
            # return render(request,'app/profile.html', context)

        else:
            context['result'] = 'Please make sure you fill in everything correctly'
        return render(request,'app/updateProfile.html', context)
    return render(request,'app/updateProfile.html', context)

def filter(request):
    context={}
    # def processForm(data):
    #     if (data.get('times')) is not None:
    #         data.times = repr(data['times'])
    if request.user.is_authenticated():
        try:

            context = {'player_id' : request.user.player.pk,
                        'login_status':request.user.username}
        except:
            context={}
    # context= {'player_id': request.user.player.pk}
    return render(request,'app/filter.html', context)

    
def match_result(request):
    context={}
    curPlayer=None
    if request.user.is_authenticated():
        try:

            context = {'player_id' : request.user.player.pk,
                        'login_status':request.user.username}
            curPlayer=request.user.player
        except:
            context={}

    context['result']=None
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
            matchesFound,partners=req.rankByScore(allPlayers,curPlayer)
            context['matchesFound']=matchesFound
            context['partners']=partners
           

            req.save()
            # context['result'] = data['gender'][0]
            
            return render(request,'app/match_result.html', context)

        else:
            context['result'] = 'Please make sure you fill in the form correctly.'
        # fix this
        return render(request,'app/filter.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        # fix this
        return render(request,'app/filter.html', context)


    # print(dict(request.POST))
    # allPlayers=Player.objects.all()
    # partners=req.rankByScore(allPlayers)

    # context={
    #     "partners": partners
    # }

    # return render(request,'app/match_result.html', context)

# youtube

def profile(request,player_id):
    context={}
    if request.user.is_authenticated():
        try:
            print('haha')

            context = {'login_status':request.user.username}

        except:
            print('didnt work')
            context={}

    try:
        
        player=Player.objects.get(pk=player_id)
        context['player']=player
        context['player_id']=request.user.player.pk

        
        

    except Player.DoesNotExist:
        raise Http404("Player does not exist")
    return render (request, 'app/profile.html',context)

# class PlayerProfileDetail(generic.DetailView):
#     model=Player
#     template_name='app/profile.html'
#     fields=('first_name','last_name','gender','andrew','email','phone','level','frequency',
#         'time')
# class PlayerProfileUpdate(UpdateView):
#     model=Player
#     fields=('first_name','last_name','gender','andrew','email','phone','level','frequency',
#         'time')

# class PlayerCreate(CreateView):
#     model=Player
#     fields=['andrew','first_name','last_name','gender','frequency']

# youtube tutorial
class UserFormView(View):
    form_class=UserForm
    template_name='app/registration_form.html'

    # display blank form
    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=self.form_class(request.POST)

        if form.is_valid():
            user=form.save(commit=False)
            # cleaned data
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User objects if credentials are correct
            user=authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    auth_login(request,user)
                    return redirect('signup')

        return render(request,self.template_name,{'form':form})

# from django documentation
def login(request):
    
    context={'result':None}
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        auth_login(request, user)
        # Redirect to a success page.
        context={'login_status':username}
        return redirect('index')
        
        # return render(request, 'app/index.html', context)
        
    else:
        context['result']="Invalid log in. Please try again."
        return render(request, 'app/login.html', context)
        # Return an 'invalid login' error message.
    return render(request, 'app/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('index')
    # return render(request, 'app/logout.html', context)
