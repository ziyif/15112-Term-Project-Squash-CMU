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


