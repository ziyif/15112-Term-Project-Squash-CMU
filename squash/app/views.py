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

# Create your views here.

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
    context['instructions'] = "Please log in to enjoy all features."
    return render(request, 'app/index.html', context)

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

def getRank(player,rankedPlayers):
    for person in rankedPlayers:
        if person[2]==player:
            return person[0]
    return None
def getIndex(player,rankedPlayers):
    for i in range(len(rankedPlayers)):
        if rankedPlayers[i][2]==player:
            return i
    return None

# player1 ranks same or lower than player 2 and player1 wins 
def getPointsGain(player1Points,player2Points):
    difference=player2Points-player1Points
    if difference==0:
        return (10,-5)
    elif difference>=100: return (50,-30)
    elif 50<=difference<100: return (25,-15)
    elif 0<difference<50: return (15,-10)
 
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

# returns outcome if player wins a match against opponent
def afterOneMatch(player,playerPoints,opponent,opponentPoints,rankedPlayers):

    gain=getPointsGain(playerPoints,opponentPoints)
    playerPoints+=gain[0]
    opponentPoints+=gain[1]
    # result is a list with points
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

 # rankedPlayers: [(1,240,player),(2,200,player)]   
def getWaysToMoveUpInLadder(player,rankedPlayers):
    curRank=getRank(player,rankedPlayers)
    index=getIndex(player,rankedPlayers)
    #  two players higher ranked apponents
    if curRank==1:
        return []
    elif curRank==2:
        n=1
    elif curRank==3:
        n=2
    else:
        n=3
    print(n)
    possibleOpponents=getPossibleOpponents(curRank,index,rankedPlayers,n)
    print(possibleOpponents)
    matchesNeeded=[]
    for opponentInfo in possibleOpponents:
        opponentCurPoints=opponentInfo[1]
        # the object opponent
        opponent=opponentInfo[2]
        count=1
        resultAfterMatch=afterOneMatch(player,player.points,opponent,opponentCurPoints,rankedPlayers)
        # rank unchanged
        while resultAfterMatch[0]==curRank:
            count+=1
            # playe one more match
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
    print(rankedPlayers)
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

# def result_confirmation(request):

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
        #     context['result'] = form.get("first_name")
         
            try:            
            # matchHistoryByTime
                player=request.user.player
                opponentAndrew=formData['opponent_andrew']
                opponent=Player.objects.get(andrew=opponentAndrew)
                winnerAndrew=formData['winner_andrew']
                winner=Player.objects.get(andrew=winnerAndrew)
                
                request.session['matchFormData']=formData
                return redirect('result_confirmation')
                # return render(request,'result_confirmation.html',context)
                # return render(request,'app/profile.html', context)
            except:
                context['result'] = 'Plase make sure you fill in the form correctly.'

        else:
            context['result'] = 'Plase make sure you fill in the form correctly.'
        return render(request,'app/enter_result.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        return render(request,'app/enter_result.html', context)

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

# match result confirmed and will be saved
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
    # matchHistoryByTime
    
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

    # matchHistoryByOpponent

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

# def success(request):
#     if request.user.is_authenticated():
#         try:

#             context = {'player_id' : request.user.player.pk,
#                         'login_status':request.user.player.first_name}
#         except:
#             context={}
    

#         context['selfGain']=selfGain
#         context['updatedPoints']=player.points
#         context['opponentGain']=opponentGain
                
                
#                 return render(request,'success.html',context)
#                 # return render(request,'app/profile.html', context)
#             except:
#                 context['result'] = 'Plase make sure you fill in the form correctly.'

#         else:
#             context['result'] = 'Plase make sure you fill in the form correctly.'
#         return render(request,'app/enter_result.html', context)

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         return render(request,'app/enter_result.html', context)




# @login_required(login_url='/login',redirect_field_name='')
# def enter_result(request):
#     if request.user.is_authenticated():
#         try:

#             context = {'player_id' : request.user.player.pk,
#                         'login_status':request.user.player.first_name}
#         except:
#             context={}
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         data = dict(request.POST)
#         # create a form instance and populate it with data from the request:
#         form = MatchScoreForm(request.POST)

#         # check whether it's valid:
#         if form.is_valid():
#             formData = form.cleaned_data
#         #     context['result'] = form.get("first_name")
#             user=request.user
#             player=user.player
#             try:            
#             # matchHistoryByTime
            
#                 opponentAndrew=formData['opponent_andrew']
#                 opponent=Player.objects.get(andrew=opponentAndrew)
#                 winnerAndrew=formData['winner_andrew']
#                 winner=Player.objects.get(andrew=winnerAndrew)

#                 # update ranking points
#                 selfGain=player.pointsGain(opponent,winnerAndrew)
#                 opponentGain=opponent.pointsGain(player,winnerAndrew)

#                 player.points+=selfGain
#                 opponent.points+=opponentGain

#                 matchResultForPlayer=(formData['match_date'],
#                                         winnerAndrew,
#                                         winner.first_name,
#                                         opponentAndrew,
#                                         opponent.id,
#                                         opponent.first_name,
#                                         opponent.last_name,
#                                         formData['match_score'],
#                                         selfGain,
#                                         opponentGain,
#                                         player.points,
#                                         opponent.points
#                                         )

#                 matchResultForOpponent=(formData['match_date'],
#                                         winnerAndrew,
#                                         winner.first_name,
#                                         player.andrew,
#                                         player.id,
#                                         player.first_name,
#                                         player.last_name,
#                                         formData['match_score'],
#                                         opponentGain,
#                                         selfGain,
#                                         opponent.points,
#                                         player.points
#                                         )

#                 # update user's match history
#                 if player.matchHistoryByTime == "None":
#                     allMatches=[]
#                 else:
#                     jsonDec = json.decoder.JSONDecoder()
#                     allMatches = jsonDec.decode(player.matchHistoryByTime)

#                 allMatches.append(matchResultForPlayer)

#                 player.matchHistoryByTime=json.dumps(allMatches)
                
#                 # update opponent's Match History
#                 if opponent.matchHistoryByTime == "None":
#                     opponentMatches =[]
#                 else:
#                     jsonDec = json.decoder.JSONDecoder()
#                     opponentMatches = jsonDec.decode(opponent.matchHistoryByTime)

#                 opponentMatches.append(matchResultForOpponent)

#                 opponent.matchHistoryByTime=json.dumps(opponentMatches)

#                 # matchHistoryByOpponent

#                 selfMatchInfo=(formData['match_date'],
#                                 winnerAndrew,
#                                 winner.first_name,
#                                 formData['match_score'],
#                                 selfGain,
#                                 opponentGain,
#                                 player.points,
#                                 opponent.points
#                                 )
#                 opponentMatchInfo=(formData['match_date'],
#                                     winnerAndrew,
#                                     winner.first_name,
#                                     formData['match_score'],
#                                     opponentGain,
#                                     selfGain,
#                                     opponent.points,
#                                     player.points
#                                     )

#                 # update for user
#                 if player.matchHistoryByOpponent== "None":
#                     matchesDict=dict()
#                 else:
#                     jsonDec = json.decoder.JSONDecoder()
#                     matchesDict = jsonDec.decode(player.matchHistoryByOpponent)
#                 if opponentAndrew in matchesDict:
#                     matchesDict[opponentAndrew].append(selfMatchInfo)
#                 else:
#                     matchesDict[opponentAndrew]=[selfMatchInfo]
#                 player.matchHistoryByOpponent=json.dumps(matchesDict)

#                 # update for user's opponent
#                 if opponent.matchHistoryByOpponent== "None":
#                     opponentDict=dict()
#                 else:
#                     jsonDec = json.decoder.JSONDecoder()
#                     opponentDict = jsonDec.decode(opponent.matchHistoryByOpponent)
#                 if player.andrew in opponentDict:
#                     opponentDict[player.andrew].append(opponentMatchInfo)
#                 else:
                    
#                     opponentDict[player.andrew]=[opponentMatchInfo]
#                 opponent.matchHistoryByOpponent=json.dumps(opponentDict)


#                 user.player.save()
#                 opponent.save()
                
                
#                 return redirect('/match_history/{}'.format(user.player.pk))
#                 # return render(request,'app/profile.html', context)
#             except:
#                 context['result'] = 'Plase make sure you fill in the form correctly.'

#         else:
#             context['result'] = 'Plase make sure you fill in the form correctly.'
#         return render(request,'app/enter_result.html', context)

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         return render(request,'app/enter_result.html', context)

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
            print(player.getConfidenceFactorAgainstOpponent(opponent))
            context['confidence_factor_against']=player.getConfidenceFactorAgainstOpponent(opponent)
        
    except Player.DoesNotExist:
        raise Http404("Player does not exist")
    return render (request, 'app/match_history_opponent.html',context)

@login_required(login_url='/login',redirect_field_name='')
def partner(request):
    context={}
    if request.user.is_authenticated():
        try:

            context = {'player_id' : request.user.player.pk,
                        'login_status':request.user.player.first_name}
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

@login_required(login_url='/login',redirect_field_name='')
def updateProfile(request):
    context={}
    if request.user.is_authenticated():
        try:

            context = {'player_id' : request.user.player.pk,
                        'login_status':request.user.player.first_name}
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
                        'login_status':request.user.player.first_name}
        except:
            context={}
    # context= {'player_id': request.user.player.pk}
    return render(request,'app/filter.html', context)

# @login_required(login_url='/login',redirect_field_name='')
# def autoMatch(request):
#     context={}
#     # def processForm(data):
#     #     if (data.get('times')) is not None:
#     #         data.times = repr(data['times'])
#     if request.user.is_authenticated():
#         try:

#             context = {'player_id' : request.user.player.pk,
#                         'login_status':request.user.player.first_name}
#         except:
#             context={}
#     # context= {'player_id': request.user.player.pk}
#     return render(request,'app/match_result.html', context) 


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
           

            # context['result'] = data['gender'][0]
            
            return render(request,'app/match_result.html', context)

        else:
            context['result'] = 'Please make sure you fill in the form correctly.'
        # fix this
        return render(request,'app/filter.html', context)

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

        # fix this
        # return render(request,'app/filter.html', context)


    # print(dict(request.POST))
    # allPlayers=Player.objects.all()
    # partners=req.rankByScore(allPlayers)

    # context={
    #     "partners": partners
    # }

    # return render(request,'app/match_result.html', context)




# Youtube
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
