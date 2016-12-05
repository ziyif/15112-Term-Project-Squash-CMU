from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
# from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# from video do i need it?
from django.core.urlresolvers import reverse
import json


#######
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from registration.signals import user_registered


class Player(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)

    andrew=models.CharField(max_length=10)
    first_name=models.CharField(max_length=30,default='None')
    last_name=models.CharField(max_length=30,default='None')

    GENDER_CHOICES=(
        ('M','Male'),
        ('F','Female')

    )
    gender=models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,

    )

    phone=models.CharField(max_length=20,default='None')
    email=models.CharField(max_length=50,default="None")
    
    LEVEL_CHOICES=(
        (1.0, 1.0),
        (1.5, 1.5),
        (2.0, 2.0),
        (2.5, 2.5),
        (3.0, 3.0),
        (3.5, 3.5),
        (4.0, 4.0),
        (4.5, 4.5),
        (5.0, 5.0),
        (5.5, 5.5),
        (6.0, 6.0)
  

    )
    level= models.DecimalField(
        max_digits=2,
        decimal_places=1,
        choices=LEVEL_CHOICES,

    )

    FREQUENCY_CHOICES=(
        (1,"Once/ week"),
        (2,"Twice/ week"),
        (3,"Three times/ week"),
        (4,"Four times/ week"),
        (5,"Five times/ week"),
        (6,"Six times/ week"),
        (7,"Everyday"),

    )

    frequency=models.IntegerField(
        choices=FREQUENCY_CHOICES

    )

    TIMES_CHOICES=(
        ('MM','Monday Morning'),
        ('MA','Monday Afternoon'),
        ('ME','Monday Evening'),
        ('TM','Tuesday Morning'),
        ('TA','Tuesday Afternoon'),
        ('TE','Tuesday Evening'),
        ('WM','Wednesday Morning'),
        ('WA','Wednesday Afternoon'),
        ('WE','Wednesday Evening'),
        ('TrM','Thursday Morning'),
        ('TrA','Thursday Afternoon'),
        ('TrE','Thursday Evening'),
        ('FM','Friday Morning'),
        ('FA','Friday Afternoon'),
        ('FE','Friday Evening'),
        ('SM','Saturday Morning'),
        ('SA','Saturday Afternoon'),
        ('SE','Saturday Evening'),
        ('SUM','Sunday Morning'),
        ('SUA','Sunday Afternoon'),
        ('SUN','Sunday Evening'),

    )

    times=models.TextField()
    points=models.IntegerField(default=0)
    matchHistoryByOpponent=models.TextField(default="None")
    matchHistoryByTime=models.TextField(default="None")
    # matchHistory=models.TextField(default="None")

    def get_absolute_url(self):
        return reverse('app.views.profile',kwargs={'pk':self.pk})
        
    def __str__(self):
        return self.first_name + " "+ self.last_name

    def assure_user_profile_exists(pk):
        """
        Creates a user profile if a User exists, but the
        profile does not exist.  Use this in views or other
        places where you don't have the user object but have the pk.
        """
        user = User.objects.get(pk=pk)
        try:
        # fails if it doesn't exist
            userprofile = user.player
        except Player.DoesNotExist:
            userprofile = Player(user=user)
            userprofile.save()
        return


    def create_user_profile(**kwargs):
        UserProfile.objects.get_or_create(user=kwargs['user'])

    user_registered.connect(create_user_profile)

    def autoMatch(self,allPlayers):
        
        result=dict()
        numOfMathces=0
        for player in allPlayers:
            fullScore=1

            # level
            # convert decimal to float
            playerLevel=float(player.level)
            selfLevel=float(self.level)
            
            levelWeight=0.5
            difference=abs(selfLevel-playerLevel)
            if difference>=2:
                score=0
            else:
                differenceWeight=0.5
                score=fullScore-difference*differenceWeight
            levelScore=levelWeight*score
            print('levelScore',levelScore)


            #timesPreferred

            jsonDec = json.decoder.JSONDecoder()
            timesList = jsonDec.decode(self.times)
            timesSet=set(timesList)

            playerTimesList = jsonDec.decode(player.times)
            playerTimes=set(playerTimesList)

            commonTimes=timesSet.union(playerTimes)
            numOfCommonBlocks=len(commonTimes)
            timesWeight=0.3
            if numOfCommonBlocks>=self.frequency:
                timesScore=fullScore*timesWeight
            else:
                timesScore=numOfCommonBlocks/self.frequency*timesWeight
            print('timesScore',timesScore)


            # frequency
            frequencyWeight=0.2
            playerFrequency=player.frequency
            selfFrequency=self.frequency
            frequencyScore=min(playerFrequency,selfFrequency)/max(playerFrequency,selfFrequency)*frequencyWeight
            print('freqScore',frequencyScore)

            scale=100
            totalScore=(levelScore+frequencyScore+timesScore)*scale
            totalScore= float("{0:.2f}".format(totalScore))

            

            goodScore=70
            if totalScore> goodScore and (player != self):
                numOfMathces+=1
                if totalScore not in result:
                    result[totalScore]={player.first_name:{'player': player,'commonTimes': commonTimes,'score':totalScore}}
                else:
                    result[totalScore][player.first_name]={'player': player,'commonTimes': commonTimes,'score':totalScore}
        # tuple: ( number of player found, dictionary with players )
        return (numOfMathces,result)

    def rankByScore(self,allPlayers):
        
        numOfMatches,matchPlayers=self.autoMatch(allPlayers)
        
        scores=[]
        for score in matchPlayers:
            # playersWithScore=len(matchPlayers[score])
            # for i in range(playersWithScore):
            scores.append(score)
        sortedScores=sorted(scores)
        sortedScores=list(reversed(sortedScores))
        rankedResult=dict()
        curRank=0
        for i in range(len(sortedScores)):
            curRank+=1
            score=sortedScores[i]
            playersWithScore=matchPlayers[score]
            # for player in playersWithScore:
            #     print('here',playersWithScore[player])
            #     playersWithScore[player].append(score)
            rankedResult[curRank]=playersWithScore
            curRank+=(len(playersWithScore)-1)
        print('rankedResult', rankedResult)
        return (numOfMatches, rankedResult)

    # def getMatchHistory(self,player):
    #     Format={'user1': [(20160102,'winnerAndrew',"3:1"),(20160103,'winnerAndrew','1:2')]}
    #     jsonDec = json.decoder.JSONDecoder()

    #     allMatches = jsonDec.decode(self.matchHistory)
    #     playerAndrew=player.andrew
    #     # list
    #     if playerAndrew in allMatches:
    #         matches=allMatches[playerAndrew]
    #         numOfMatches=len(matches)
    #         rankedMatches=rankByDate(matches)
    #         return rankedMatches
    #     else:
    #         return []

    # def rankByDate(matches):
    #     return sorted(matches,key=lambda x: x[0])

    # def findPercentageOfWins(self,player,rankedMatches):
    #     totalMatches=len(rankedMatches)
    #     for match in rankedMatches:
    #         if match[1]==self.andrew:
    #             numOfWin+=1
    #     return numOfWin/totalMatches


    # def pointsGain(self,player,result,rankedMatches):
    #     # rank lower and loses, no gain no loss
    #     if self.points<=player.points and result[1]==player.andrew:
    #         return 0

    #     # rank lower and wins
    #     elif self.points<=player.points and result[1]==self.andrew:
    #         percentageOfWins=findPercentageOfWins(self,player,rankedMatches)

    #############
    #Match Result, Scoring systems

    def getAllMatchHistory(self):
        jsonDec = json.decoder.JSONDecoder()
        allMatches = jsonDec.decode(self.matchHistoryByTime)
        rankedMatches=rankByDate(allMatches)
        return rankedMatches

    def getMatchHistoryAgainstOpponent(self,player):
        # Format={'user1': [(20160102,'winnerAndrew',"3:1"),(20160103,'winnerAndrew','1:2')]}
        jsonDec = json.decoder.JSONDecoder()

        allMatches = jsonDec.decode(self.matchHistoryByOpponent)
        playerAndrew=player.andrew
        # list
        if playerAndrew in allMatches:
            matches=allMatches[playerAndrew]
            numOfMatches=len(matches)
            rankedMatches=rankByDate(matches)
            return rankedMatches
        else:
            return []

    def rankByDate(matches):
        rankedMatches=sorted(matches,key=lambda x: x[0])
        rankedMatches=rankedMatches[::-1]
        return rankedMatches

    def findPercentageOfWins(self,matches):
        totalMatches=len(matches)
        if totalMatches==0:
            return None
        for match in matches:
            if match[1]==self.andrew:
                numOfWin+=1
        return numOfWin/totalMatches

    def getDate():
        today=datetime.datetime.today()
        year=str(today.year)
        month=str(today.month)
        if len(month)==1:
            month="0"+month
        day=str(today.day)
        if len(day)==1:
            day="0"+day
        date=year+month+day
        return eval(date)

    def dateOfNMonthsAgo(n):
        thisDay=datetime.date.today() - datetime.timedelta(n*365/12)
        year=str(thisDay.year)
        month=str(thisDay.month)
        if len(month)==1:
            month="0"+month
        day=str(thisDay.day)
        if len(day)==1:
            day="0"+day
        date=year+month+day
        return eval(date)

        
    def getRecentMatches(rankedMatches,n):
        currentDate=getDate()
        dateOfNMonthsAgo=dateOfNMonthsAgo(n)
        result=[]
        for i in range (len(rankedMatches)):
            match=rankedMatches[i]
            dateOfMatch=match[0]
            if dateOfMatch>=dateOfNMonthsAgo:
                result.append(match)
            else:
                break
        return result


    def getActivityScore(self,timePeriod):
        allMatches=self.getAllMatchHistory()
        # activity in 3 months
        recentMathces=getRecentMatches(allMatches,timePeriod)
        numOfRecentMatches=len(recentMathces)
        if numOfRecentMatches==0:
            return 0
        else:
            return 1-1/numOfRecentMatches

    def getConfidenceFactorAgainstOpponent(self,player):
        
        selfActivityScore=self.getActivityScore(5)
        playerActivityScore=player.getActivityScore(5)
        activityScore= selfActivityScore/ (selfActivityScore+playerActivityScore)

        selfPoints= self.points
        playerPoints= player.points
        difference=selfPoints-playerPoints
        if difference>=100:
            rankingScore=1
        elif 0<difference<100:
            rankingScore=1*difference/100
        else: 
            rankingScore=0

        scale=100
        # if have not played with player
        if numOfTotalMatches==0:
            mostRecentMatchScore=0
            totalScore=mostRecentMatchScore*0.1+activityScore*0.2+rankingScore*0.7
            return scale*totalScore

        matchesAgainstOpponent=self.getMatchHistoryAgainstOpponent(player)
        numOfTotalMatches=len(matchesAgainstOpponent)

        # recent 5 months
        recentMatches=getRecentMatches(matchesAgainstOpponent,5)
        numOfRecentMatches=len(recentMatches)

        totalPercentageOfWins=self.findPercentageOfWins(matchesAgainstOpponent)
        recentPercentageOfWins=self.findPercentageOfWins(recentMatches)

        mostRecentMatchWinner=matchesAgainstOpponent[0][1]
        if mostRecentMatchWinner==self.andrew:
            mostRecentMatchScore=1
        else:
            mostRecentMatchScore=0


        if numOfRecentMatches>=2:
            percentageOfWinsScore=0.8*recentPercentageOfWins+0.2*totalPercentageOfWins
        elif numOfRecentMatches==1:
            percentageOfWinsScore=0.6*recentPercentageOfWins+0.4*totalPercentageOfWins
        # have not played with player recently
        elif numOfRecentMatches==0:
            recentPercentageOfWins=0
            percentageOfWinsScore==0.2*recentPercentageOfWins+0.8*totalPercentageOfWins

        if 1<=numOfTotalMatches<3:
            return (0.1*mostRecentMatchScore+0.4*percentageOfWinsScore+0.2*activityScore
                        +0.3*rankingScore)
        elif totalMatches>=3:
            return (0.1*mostRecentMatchScore+0.5*percentageOfWinsScore+0.2*activityScore
                        +0.2*rankingScore)


    def getOverallConfidenceFactor(self):
        allMatches=self.getAllMatchHistory()
        recentMatches=getRecentMatches(allMatches,5)
        percentageOfWins=self.findPercentageOfWins(recentMatches)
        activity_in_five_months=self.getActivityScore(5)
        activity_in_three_months=self.getActivityScore(3)
        activityScore=0.4*activity_in_five_months+0.6*activity_in_three_months

        totalScore=0.6*percentageOfWins+0.4*activityScore
        scale=100

        return totalScore*scale



    def pointsGain(self,player,result,rankedMatches):
        pointsDifference=abs(self.points-player.points)

        # rank lower and loses, no gain no loss
        if self.points<player.points and result[1]==player.andrew:
            return 0

        # rank lower and wins
        elif self.points<player.points and result[1]==self.andrew:
            if pointsDifference>=100:
                return 50
            elif 50<=pointsDifference<100:
                return 25
            elif pointsDifference<50:
                return 15
        # rank higher and wins
        elif self.points>player.points and result[1]==self.andrew:
            if pointsDifference<=20:
                return 5
            else: 
                return 0

        # rank higher and loses:
        elif self.points>player.points and result[1]==player.andrew:
            if pointsDifference>=100:
                return -30
            elif 50<=pointsDifference<100:
                return -15
            elif pointsDifference<50:
                return -10

        # rank same and wins:
        elif self.points == player.points and result[1]== self.andrew:
            return 10

        # rank same and loses:
        elif self.points == player.points and result[1]== player.andrew:
            return -5
        
        



class Requirements(models.Model):
    GENDER_CHOICES=(
        ('M','Male'),
        ('F','Female')

    )
    gender=models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,

    )
    IMPORTANCE_CHOICES=(
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5)
    )

    gender_importance=models.IntegerField(choices=IMPORTANCE_CHOICES,null=True)

    
    LEVEL_CHOICES=(
        (1.0, 1.0),
        (1.5, 1.5),
        (2.0, 2.0),
        (2.5, 2.5),
        (3.0, 3.0),
        (3.5, 3.5),
        (4.0, 4.0),
        (4.5, 4.5),
        (5.0, 5.0),
        (5.5, 5.5),
        (6.0, 6.0)
  

    )
    min_level= models.DecimalField(
        max_digits=2,
        decimal_places=1,
        choices=LEVEL_CHOICES,

    )
    max_level= models.DecimalField(
        max_digits=2,
        decimal_places=1,
        choices=LEVEL_CHOICES,

    )

    level_importance=models.IntegerField(choices=IMPORTANCE_CHOICES,null=True)

    FREQUENCY_CHOICES=(
        (1,"Once/ week"),
        (2,"Twice/ week"),
        (3,"Three times/ week"),
        (4,"Four times/ week"),
        (5,"Five times/ week"),
        (6,"Six times/ week"),
        (7,"Everyday"),

    )

    frequency=models.IntegerField(
        choices=FREQUENCY_CHOICES

    )
    frequency_importance=models.IntegerField(choices=IMPORTANCE_CHOICES,null=True)
    TIMES_CHOICES=(
        ('MM','Monday Morning'),
        ('MA','Monday Afternoon'),
        ('MN','Monday Night'),
        ('TM','Tuesday Morning'),
        ('TA','Tuesday Afternoon'),
        ('TN','Tuesday Night'),
        ('WM','Wednesday Morning'),
        ('WA','Wednesday Afternoon'),
        ('WN','Wednesday Night'),
        ('TrM','Thursday Morning'),
        ('TrA','Thursday Afternoon'),
        ('TrN','Thursday Night'),
        ('FM','Friday Morning'),
        ('FA','Friday Afternoon'),
        ('FN','Friday Night'),
        ('SM','Saturday Morning'),
        ('SA','Saturday Afternoon'),
        ('SN','Saturday Night'),
        ('SuM','Sunday Morning'),
        ('SUA','Sunday Afternoon'),
        ('SUN','Sunday Night'),

    )

    times=models.TextField()
    times_importance=models.IntegerField(choices=IMPORTANCE_CHOICES,null=True)

    
    def filter(self,allPlayers,curPlayer=None):
        
        jsonDec = json.decoder.JSONDecoder()
        timesList = jsonDec.decode(self.times)
        timesSet=set(timesList)
        requirements={
                        'gender':self.gender,
                        'min_level': self.min_level,
                        'max_level': self.max_level,
                        'timesPreferred':timesSet,
                        'frequency': self.frequency,
                        'importance': {
                            'gender': self.gender_importance,
                            'times': self.times_importance,
                            'level': self.level_importance,
                            'frequency': self.frequency_importance,
                        }
                    }

        result=dict()
        numOfMathces=0
        for player in allPlayers:
            # list 
            
            
            importance=requirements['importance']  # dictionary

            totalImportanceScore=0

            for key in importance:
                
                totalImportanceScore+=importance[key]


            # gender
            if player.gender==requirements['gender']:
                weightA=importance['gender']/totalImportanceScore
                scoreA= 1*weightA
            else:
                scoreA=0

            # level
            # convert decimal to float
            playerLevel=float(player.level)
            min_level=float(requirements['min_level'])
            max_level=float(requirements['max_level'])
            weightB=importance['level']/totalImportanceScore
            if min_level<=playerLevel<=max_level:
                scoreB= 1* weightB
            elif playerLevel<min_level:
                scoreB=1*(1/3)**(min_level-playerLevel)*weightB


            #timesPreferred
            requirementTime=requirements['timesPreferred']

            frequency=requirements['frequency']


            jsonDec = json.decoder.JSONDecoder()
            playerTimesList = jsonDec.decode(player.times)
            playerTimes=set(playerTimesList)

            commonTimes=requirementTime.union(playerTimes)
            numOfCommonBlocks=len(commonTimes)
            weightC=importance['times']/totalImportanceScore
            if numOfCommonBlocks>=frequency:
                scoreC=1*weightC
            else:
                scoreC=numOfCommonBlocks/frequency*weightC


            # frequency
            weightD=importance['frequency']/totalImportanceScore
            playerFrequency=player.frequency
            scoreD=min(playerFrequency,frequency)/max(playerFrequency,frequency)*weightD

            scale=100
            totalScore=(scoreA+scoreB+scoreC+scoreD)*scale
            totalScore= float("{0:.2f}".format(totalScore))

            

            goodScore=70
            if totalScore> goodScore and (player != curPlayer):
                numOfMathces+=1
                if totalScore not in result:
                    result[totalScore]={player.first_name:{'player': player,'commonTimes': commonTimes,'score':totalScore}}
                else:
                    result[totalScore][player.first_name]={'player': player,'commonTimes': commonTimes,'score':totalScore}
        # tuple: ( number of player found, dictionary with players )
        return (numOfMathces,result)

    def rankByScore(self,allPlayers,curPlayer=None):
        
        numOfMatches,matchPlayers=self.filter(allPlayers,curPlayer)
        
        scores=[]
        for score in matchPlayers:
            # playersWithScore=len(matchPlayers[score])
            # for i in range(playersWithScore):
            scores.append(score)
        sortedScores=sorted(scores)
        sortedScores=list(reversed(sortedScores))
        rankedResult=dict()
        curRank=0
        for i in range(len(sortedScores)):
            curRank+=1
            score=sortedScores[i]
            playersWithScore=matchPlayers[score]
            # for player in playersWithScore:
            #     print('here',playersWithScore[player])
            #     playersWithScore[player].append(score)
            rankedResult[curRank]=playersWithScore
            curRank+=(len(playersWithScore)-1)
        print('rankedResult', rankedResult)
        return (numOfMatches, rankedResult)




# class PlayerForm(forms.ModelForm):
    
#     class Meta:

#         error_messages = {
#             NON_FIELD_ERRORS: {
#                 'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
#             }
#         }
#         model= Player
#         fields=['first_name','last_name','phone','andrew','email']
#         # fields="__all__"
#         #['first_name','last_name','gender','phone','andrew','email','level','times','frequency']


