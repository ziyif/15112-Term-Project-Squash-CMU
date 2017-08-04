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

from .forms import NameForm, RequirementsForm,UserForm,MatchScoreForm

from .models import Player,Requirements
import json

##############
# Code below are all based on Django Documentation
# https://docs.djangoproject.com/en/1.10/

# home page
def test():
    return
    
def index(request):
    context={}
    players=Player.objects.all()

    if request.user.is_authenticated():
        try:

            context = {'player_id' : request.user.player.pk,
                        'login_status':request.user.player.first_name}
        except:
            context={}
    context['greetings'] = "Welcom!"
    context['instructions'] = "Please log in to enjoy the features."
    return render(request, 'app/index.html', context)

#### 
# The following functions are for the ladder feature

# rank players according to ranking points
def rankAllPlayers(players):
    playerPoints=[]
    for player in players:
        playerPoints.append((player.points,player))
    pointsList=sorted(playerPoints,key=lambda x: x[0])
    hightToLow=list(reversed(pointsList))
    rankedResult=[]
    count=1
    prevRank=0
    prevScore=-100
    for i in range(len(hightToLow)):
        score=hightToLow[i][0]
        player=hightToLow[i][1]
        if score==prevScore:
            rank=prevRank
            count+=1
        else:
            rank=prevRank+count
            count=1
            prevRank=rank
            prevScore=score
        rankedResult.append((rank,score,player))
    return rankedResult

# returns the rank of a particular user
def getRank(player,rankedPlayers):
    for person in rankedPlayers:
        if person[2]==player:
            return person[0]
    return None

# returns the index of the user in the list
def getIndex(player,rankedPlayers):
    for i in range(len(rankedPlayers)):
        if rankedPlayers[i][2]==player:
            return i
    return None


# this function returns a tuple of points gain 
# in the condition that player1 ranks same or lower than player 2 
# and player1 wins
def getPointsGain(player1Points,player2Points):
    difference=player2Points-player1Points
    if difference==0: return (10,-5)
    elif difference>=100: return (50,-30)
    elif 50<=difference<100: return (25,-15)
    elif 0<difference<50: return (15,-10)
 
# this function returns the rank of a player, given his/her points and a list 
# of all ranking points
def getNewRank(points,resultList):
    highToLow=list(reversed(sorted(resultList)))
    count=1
    prevRank=0
    prevScore=-100
    for score in highToLow:
        if score==prevScore:
            rank=prevRank
            count+=1
        else:
            rank=prevRank+count
            count=1
            prevRank=rank
            prevScore=score
        if score==points:
            return rank

# returns outcome if player wins a match against a certain opponent
def afterOneMatch(player,playerPoints,opponent,opponentPoints,rankedPlayers):

    gain=getPointsGain(playerPoints,opponentPoints)
    playerPoints+=gain[0]
    opponentPoints+=gain[1]
    # result is a list with integers that represent ranking points
    result=[]
    for person in rankedPlayers:
        if person[2]==player:
            result.append(playerPoints)
        elif person[2]==opponent:
            result.append(opponentPoints)
        else:
            result.append(person[1])
    newRank=getNewRank(playerPoints,result)

    return (newRank,playerPoints,opponentPoints)

# returns all possible opponents of a player, given that he/she can 
# only challenge players with in n ranking places above him/her
def getPossibleOpponents(curRank,index,rankedPlayers,n):
    delta=1
    result=[]
    differenceInRank=0
    while differenceInRank<=n:
        if index-delta<0: break
        differenceInRank=curRank-rankedPlayers[index-delta][0]
        if differenceInRank==0:
            delta+=1
        elif differenceInRank==n+1:
            break
        else:
            result.append(rankedPlayers[index-delta])
            delta+=1
    return result

# rankedPlayers is a list of the format: [(1,240,player),(2,200,player)]   
def getWaysToMoveUpInLadder(player,rankedPlayers):
    curRank=getRank(player,rankedPlayers)
    index=getIndex(player,rankedPlayers)

    #  two players higher ranked apponents

    if curRank==1:
        return []
    elif curRank==2:
        # if rank is two, player can challenge 1 person
        n=1
    elif curRank==3:
        # player can challenge 2 persons
        n=2
    else:
        # player can challenge 3 persons (rule of ladder is player
        # can only challenge players within 3 ranks above)
        n=3

    possibleOpponents=getPossibleOpponents(curRank,index,rankedPlayers,n)

    matchesNeeded=[]
    for opponentInfo in possibleOpponents:
        opponentCurPoints=opponentInfo[1]
        # opponent is an object Player
        opponent=opponentInfo[2]
        count=1
        resultAfterMatch=afterOneMatch(player,player.points,opponent,opponentCurPoints,rankedPlayers)
        # while rank unchanged
        while resultAfterMatch[0]==curRank:
            # num of matches needed to player increase by 1
            count+=1
            # play one more match
            newPoints=resultAfterMatch[1]
            opponentNewPoints=resultAfterMatch[2]
            resultAfterMatch=afterOneMatch(player,newPoints,opponent,opponentNewPoints,rankedPlayers)
        matchesNeeded.append((opponent,count))
    return matchesNeeded


    
@login_required(login_url='/login',redirect_field_name='')
def ladder(request):
    context={}
    if request.user.is_authenticated():
        try:

            context = {'player_id' : request.user.player.pk,
                        'login_status':request.user.player.first_name}
        except:
            context={}
    player=request.user.player

    players=Player.objects.all()
    rankedPlayers=rankAllPlayers(players)
    context['ladder']=rankedPlayers
    rank=getRank(player,rankedPlayers)
    context['rank']=rank
    if rank==1:
        context['challenge_matches']=None
    else:
        ways=getWaysToMoveUpInLadder(player,rankedPlayers)
        context['num']=len(ways)
        context['challenge_matches']=ways

    return render(request,'app/ladder.html', context)


@login_required(login_url='/login',redirect_field_name='')
def enter_result(request):
    if request.user.is_authenticated():
        try:

            context = {'player_id' : request.user.player.pk,
                        'login_status':request.user.player.first_name}
        except:
            context={}
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        data = dict(request.POST)
        # create a form instance and populate it with data from the request:
        form = MatchScoreForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            formData = form.cleaned_data
         
            try:            
            # matchHistoryByTime
                player=request.user.player
                opponentAndrew=formData['opponent_andrew']
                opponent=Player.objects.get(andrew=opponentAndrew)
                winnerAndrew=formData['winner_andrew']
                winner=Player.objects.get(andrew=winnerAndrew)
                
                request.session['matchFormData']=formData
                return redirect('result_confirmation')
            except:
                context['result'] = 'Plase make sure you fill in the form correctly.'

        else:
            context['result'] = 'Plase make sure you fill in the form correctly.'
        return render(request,'app/enter_result.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        return render(request,'app/enter_result.html', context)

@login_required(login_url='/login',redirect_field_name='')
def result_confirmation(request):
    if request.user.is_authenticated():
        try:

            context = {'player_id' : request.user.player.pk,
                        'login_status':request.user.player.first_name}
        except:
            context={}
    formData=request.session['matchFormData']
    context['date']=formData['match_date']
    context['opponent_andrew']=formData['opponent_andrew']
    context['winner']=formData['winner_andrew']
    context['score']=formData['match_score']
  

    return render(request,'app/result_confirmation.html', context)

@login_required(login_url='/login',redirect_field_name='')
# goes to success page if match result confirmed and will be saved
def success(request):
    if request.user.is_authenticated():
        try:

            context = {'player_id' : request.user.player.pk,
                        'login_status':request.user.player.first_name}
        except:
            context={}


    formData=request.session['matchFormData']

    user=request.user
    player=user.player   

    # update matchHistoryByTime
    opponentAndrew=formData['opponent_andrew']
    opponent=Player.objects.get(andrew=opponentAndrew)
    winnerAndrew=formData['winner_andrew']
    winner=Player.objects.get(andrew=winnerAndrew)

    # update ranking points
    selfGain=player.pointsGain(opponent,winnerAndrew)
    opponentGain=opponent.pointsGain(player,winnerAndrew)

    player.points+=selfGain
    opponent.points+=opponentGain

    matchResultForPlayer=(formData['match_date'],
                            winnerAndrew,
                            winner.first_name,
                            opponentAndrew,
                            opponent.id,
                            opponent.first_name,
                            opponent.last_name,
                            formData['match_score'],
                            selfGain,
                            opponentGain,
                            player.points,
                            opponent.points
                            )

    matchResultForOpponent=(formData['match_date'],
                            winnerAndrew,
                            winner.first_name,
                            player.andrew,
                            player.id,
                            player.first_name,
                            player.last_name,
                            formData['match_score'],
                            opponentGain,
                            selfGain,
                            opponent.points,
                            player.points
                            )

    # update user's match history
    if player.matchHistoryByTime == "None":
        allMatches=[]
    else:
        jsonDec = json.decoder.JSONDecoder()
        allMatches = jsonDec.decode(player.matchHistoryByTime)

    allMatches.append(matchResultForPlayer)
    allMatches=player.rankByDate(allMatches)

    player.matchHistoryByTime=json.dumps(allMatches)
    
    # update opponent's Match History
    if opponent.matchHistoryByTime == "None":
        opponentMatches =[]
    else:
        jsonDec = json.decoder.JSONDecoder()
        opponentMatches = jsonDec.decode(opponent.matchHistoryByTime)

    opponentMatches.append(matchResultForOpponent)
    opponentMatches=opponent.rankByDate(opponentMatches)

    opponent.matchHistoryByTime=json.dumps(opponentMatches)

    # update matchHistoryByOpponent

    selfMatchInfo=(formData['match_date'],
                    winnerAndrew,
                    winner.first_name,
                    formData['match_score'],
                    selfGain,
                    opponentGain,
                    player.points,
                    opponent.points
                    )
    opponentMatchInfo=(formData['match_date'],
                        winnerAndrew,
                        winner.first_name,
                        formData['match_score'],
                        opponentGain,
                        selfGain,
                        opponent.points,
                        player.points
                        )

    # update for user
    if player.matchHistoryByOpponent== "None":
        matchesDict=dict()
    else:
        jsonDec = json.decoder.JSONDecoder()
        matchesDict = jsonDec.decode(player.matchHistoryByOpponent)
    if opponentAndrew in matchesDict:
        matchesDict[opponentAndrew].append(selfMatchInfo)
        matchesDict[opponentAndrew]=player.rankByDate(matchesDict[opponentAndrew])
    else:
        matchesDict[opponentAndrew]=[selfMatchInfo]
    player.matchHistoryByOpponent=json.dumps(matchesDict)

    # update for user's opponent
    if opponent.matchHistoryByOpponent== "None":
        opponentDict=dict()
    else:
        jsonDec = json.decoder.JSONDecoder()
        opponentDict = jsonDec.decode(opponent.matchHistoryByOpponent)
    if player.andrew in opponentDict:
        opponentDict[player.andrew].append(opponentMatchInfo)
        opponentDict[player.andrew]=opponent.rankByDate(opponentDict[player.andrew])
    else:
        opponentDict[player.andrew]=[opponentMatchInfo]
    opponent.matchHistoryByOpponent=json.dumps(opponentDict)


    user.player.save()
    opponent.save()
  
    context['selfGain']=selfGain
    context['updatedPoints']=player.points
    context['opponentGain']=opponentGain
                            
    return render(request,'app/success.html',context)


@login_required(login_url='/login',redirect_field_name='')
def match_history(request,player_id):
    context={}
    if request.user.is_authenticated():
        try:
            context = {'player_id' : request.user.player.pk,
                        'login_status':request.user.player.first_name}
        except:
            context={}
    try:
        player=Player.objects.get(pk=player_id)
        context['player']=player
        context['player_id']=request.user.player.pk
        if player.matchHistoryByTime=="None":
            context['result']="You have no recorded matches."
            context['confidence_factor']='Not Applicable'
        else:
            jsonDec = json.decoder.JSONDecoder()
            allMatches = jsonDec.decode(player.matchHistoryByTime)
            confidenceFactor=player.getOverallConfidenceFactor()
            context['matches']=allMatches

            context['totalMatches']=len(allMatches)
            context['numOfWins']=player.findNumOfWins(allMatches)
            recentMatches=player.getRecentMatches(allMatches,3)
            context['recentMatches']=len(recentMatches)
            context['confidence_factor']=confidenceFactor
        
    except Player.DoesNotExist:
        raise Http404("Player does not exist")
    return render (request, 'app/match_history.html',context)

@login_required(login_url='/login',redirect_field_name='')
def match_history_opponent(request,player_id,opponent_id):
    context={}
    if request.user.is_authenticated():
        try:
            context = {'player_id' : request.user.player.pk,
                        'login_status':request.user.player.first_name}

        except:
            context={}

    try:    
        player=Player.objects.get(pk=player_id)
        opponent=Player.objects.get(pk=opponent_id)

        matches=player.getMatchHistoryAgainstOpponent(opponent)
        if len(matches)==0:
            context['player']=player
            context['opponent']=opponent
            context['result']="You have no recorded matches."
            context['confidence_factor_against']='Not Applicable'
        else:

            recent_matches=player.getRecentMatches(matches,5)
            context['player']=player
            context['opponent']=opponent
            context['player_id']=request.user.player.pk
            context['numMatches']=len(matches)
            context['total_percent']=int(100*(player.findPercentageOfWins(matches)))
            if player.findPercentageOfWins(recent_matches)==None:
                context['recent_percent']=None
            else:
                context['recent_percent']=int(100*(player.findPercentageOfWins(recent_matches)))
            context['matches']=matches
            context['confidence_factor_against']=player.getConfidenceFactorAgainstOpponent(opponent)
        
    except Player.DoesNotExist:
        raise Http404("Player does not exist")
    return render (request, 'app/match_history_opponent.html',context)

@login_required(login_url='/login',redirect_field_name='')
# find a partner page
def partner(request):
    context={}
    if request.user.is_authenticated():
        try:

            context = {'player_id' : request.user.player.pk,
                        'login_status':request.user.player.first_name}
        except:
            context={}

    return render(request,'app/partner.html', context)

# some ideas used here adapted from http://stackoverflow.com/questions/1110153/what-is-the-most-efficent-way-to-store-a-list-in-the-django-models
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

            user.player.save()
            
            context['result'] = data['first_name'][0]
            return redirect('/user/{}'.format(user.player.pk))

        else:
            context['result'] = 'Plase make sure you fill in the form correctly.'
        return render(request,'app/signup.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        return render(request,'app/signup.html', context)

@login_required(login_url='/login',redirect_field_name='')
def updateProfile(request):
    context={}
    if request.user.is_authenticated():
        try:

            context = {'player_id' : request.user.player.pk,
                        'login_status':request.user.player.first_name}
        except:
            context={}

    if request.method == 'POST':
        data = dict(request.POST)
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            formData = form.cleaned_data
        #     context['result'] = form.get("first_name")
            player=request.user.player
            player.first_name=formData['first_name']
            player.last_name=formData['last_name']
            player.gender=formData['gender']
            player.andrew=formData['andrew']
            player.phone==formData['phone']
            player.email=formData['email']
            player.level=formData['level']
            player.frequency=formData['frequency']
            player.times=json.dumps(data['times'])

            player.save()
            
            context['result'] = data['first_name'][0]
            
            return redirect('/user/{}'.format(user.player.pk))

        else:
            context['result'] = 'Please make sure you fill in everything correctly'
        return render(request,'app/updateProfile.html', context)
    return render(request,'app/updateProfile.html', context)

@login_required(login_url='/login',redirect_field_name='')
# manual match
def filter(request):
    context={}
    if request.user.is_authenticated():
        try:

            context = {'player_id' : request.user.player.pk,
                        'login_status':request.user.player.first_name}
        except:
            context={}

    return render(request,'app/filter.html', context)


@login_required(login_url='/login',redirect_field_name='')
def match_result(request):
    context={}
    curPlayer=None
    if request.user.is_authenticated():
        try:

            context = {'player_id' : request.user.player.pk,
                        'login_status':request.user.player.first_name}
            curPlayer=request.user.player
        except:
            context={}

    context['result']=None
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        data = dict(request.POST)

        # create a form instance and populate it with data from the request:
        form = RequirementsForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            formData = form.cleaned_data

            req=Requirements(gender=formData['gender'],
                gender_importance=formData['gender_importance'],
                min_level=formData['min_level'],
                max_level=formData['max_level'],
                level_importance=formData['level_importance'],
                frequency=formData['frequency'],
                frequency_importance=formData['frequency_importance'],
                times=json.dumps(data['times']),
                times_importance=formData['times_importance'])


            allPlayers=Player.objects.all()
            matchesFound,partners=req.rankByScore(allPlayers,curPlayer)
            context['matchesFound']=matchesFound
            context['partners']=partners

            
            return render(request,'app/match_result.html', context)

        else:
            context['result'] = 'Please make sure you fill in the form correctly.'
            return redirect('filter')

    # if a GET (or any other method) we'll create a blank form
    else:
        if request.user.is_authenticated(): 

            curPlayer=request.user.player
            allPlayers=Player.objects.all()
            matchesFound,partners=curPlayer.rankByScore(allPlayers)
            context['matchesFound']=matchesFound
            context['partners']=partners
            return render(request,'app/match_result.html', context)
        else: return redirect('login')



# From tutorial: https://www.youtube.com/watch?v=3UEY0ZIQ9dU&index=34&list=PL6gx4Cwl9DGBlmzzFcLgDhKTTfNLfX1IK
@login_required(login_url='/login',redirect_field_name='')
def profile(request,player_id):
    context={}
    if request.user.is_authenticated():
        try:
            context = {'login_status':request.user.player.first_name}

        except:
            context={}
    try:
        player=Player.objects.get(pk=player_id)
        if request.user.player==player:

            context['allowUpdate']=True
        
        context['player']=player
        context['player_id']=request.user.player.pk
        jsonDec = json.decoder.JSONDecoder()
        timesList = jsonDec.decode(player.times)
        timesSet=set(timesList)
        context['preferred_times']=timesSet
        
        
    except Player.DoesNotExist:
        raise Http404("Player does not exist")
    return render (request, 'app/profile.html',context)


# From youtube tutorial: https://www.youtube.com/watch?v=eMGtdtNR4es&list=PL6gx4Cwl9DGBlmzzFcLgDhKTTfNLfX1IK&index=36
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
# https://docs.djangoproject.com/en/1.10/
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
                
    else:
        context['result']="Invalid log in. Please try again."
        return render(request, 'app/login.html', context)
        # Return an 'invalid login' error message.
    return render(request, 'app/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('index')
