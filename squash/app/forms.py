from django.contrib.auth.models import User
from django import forms
from .models import Player

# Code below are all based on Django Documentation
# https://docs.djangoproject.com/en/1.10/

GENDER_CHOICES=(
        ('M','Male'),
        ('F','Female'),
        ('D',"Don't Care")

    )

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
        ('SUE','Sunday Evening'),

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
IMPORTANCE_CHOICES=(
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5)
    )

class NameForm(forms.Form):
    first_name = forms.CharField(label='first_name', max_length=100)
    last_name=forms.CharField(label='last_name', max_length=30)
    andrew=forms.CharField(label='andrew', max_length=10)

    gender=forms.CharField(
            label='gender', max_length=10)
    # widget=forms.Select(choices=GENDER_CHOICES))
    phone=forms.CharField(label='phone', max_length=20)
    email=forms.CharField(label='email', max_length=50)
    level= forms.DecimalField(label='level',max_digits=2,decimal_places=1,
        widget=forms.Select(choices=LEVEL_CHOICES))
    frequency=forms.IntegerField(label='frequency',
        widget=forms.Select(choices=FREQUENCY_CHOICES))
    times=forms.CharField(label='times',widget=forms.Select(choices=TIMES_CHOICES))

class MatchScoreForm(forms.Form):
    match_date= forms.IntegerField(label='match_date')
    match_score=forms.CharField(label='match_score',max_length=10)
    opponent_andrew=forms.CharField(label='opponent_andrew',max_length=20)
    winner_andrew=forms.CharField(label='winner_andrew', max_length=20)


class RequirementsForm(forms.Form):
    gender=forms.CharField(
            label='gender', max_length=10,
            widget=forms.Select(choices=GENDER_CHOICES))
    min_level= forms.DecimalField(label='min_level',max_digits=2,decimal_places=1,
        widget=forms.Select(choices=LEVEL_CHOICES))
    max_level= forms.DecimalField(label='max_level',max_digits=2,decimal_places=1,
        widget=forms.Select(choices=LEVEL_CHOICES))
    frequency=forms.IntegerField(label='frequency',
        widget=forms.Select(choices=FREQUENCY_CHOICES))
    times=forms.CharField(label='times',widget=forms.Select(choices=TIMES_CHOICES))


    gender_importance=forms.IntegerField(label='gender_importance',
        widget=forms.Select(choices=IMPORTANCE_CHOICES))
    level_importance=forms.IntegerField(label='level_importance',
        widget=forms.Select(choices=IMPORTANCE_CHOICES))

    frequency_importance=forms.IntegerField(label='frequency_importance',
        widget=forms.Select(choices=IMPORTANCE_CHOICES))
    times_importance=forms.IntegerField(label='times_importance',
        widget=forms.Select(choices=IMPORTANCE_CHOICES))
 
class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
        
    class Meta:
        model=User
        fields=['username']


