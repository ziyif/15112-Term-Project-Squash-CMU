from django.db import models
from django.forms import ModelForm
# from django.core.exceptions import NON_FIELD_ERRORS


# from video do i need it?
from django.core.urlresolvers import reverse
import json


class Player(models.Model):
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
        ('SuA','Sunday Afternoon'),
        ('SuN','Sunday Night'),

    )

    times=models.TextField()

    def get_absolute_url(self):
        return reverse('app:profile',kwargs={'pk':self.pk})
        
    def __str__(self):
        return self.first_name + " "+ self.last_name


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
        ('SuA','Sunday Afternoon'),
        ('SuN','Sunday Night'),

    )

    times=models.TextField()
    times_importance=models.IntegerField(choices=IMPORTANCE_CHOICES,null=True)

    
    def filter(self,allPlayers):
        jsonDec = json.decoder.JSONDecoder()
        timesList = jsonDec.decode(self.times)
        timesSet=set(timesList)
        requirements={
                        'gender':self.gender,
                        'min_level': eval(self.min_level),
                        'max_level': eval(self.max_level),
                        'timesPreferred':timesSet,
                        'frequency': int(self.frequency),
                        'importance': {
                            'gender': int(self.gender_importance),
                            'times': int(self.times_importance),
                            'level': int(self.level_importance),
                            'frequency': int(self.frequency_importance),
                        }
                    }

        result=dict()
        for player in allPlayers:
            # list 
            
            
            importance=requirements['importance']  # dictionary

            totalImportanceScore=0

            for key in importance:
                print(importance[key])
                totalImportanceScore+=importance[key]


            # gender
            if player.gender==requirements['gender']:
                weightA=importance['gender']/totalImportanceScore
                scoreA= 1*weightA
            else:
                scoreA=0

            # level
            playerLevel=player.level
            min_level=requirements['min_level']
            max_level=requirements['max_level']
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

            totalScore=scoreA+scoreB+scoreC+scoreD

            if totalScore> 0.7:
                if totalScore not in result:
                    result[totalScore]={player:commonBlocks}
                else:
                    result[totalScore][player]=commonBlocks

            return result

    def rankByScore(self,allPlayers):
        matchPlayers=self.filter(allPlayers)
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
            playersWithScore=matchPlayers[sortedScores[i]]
            for player in playersWithScore:
                playersWithScore[player].append(score)
            rankedResult[curRank]=playersWithScore
            curRangk+=(len(playersWithScore)-1)
        return rankedResult


            

































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


