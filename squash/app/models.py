from django.db import models

# from video do i need it?
from django.core.urlresolvers import reverse


class Player(models.Model):
    andrew=models.CharField(max_length=10)
    first_name=models.CharField(max_length=30,default='None')
    last_name=models.CharField(max_length=30,default='None')

    Gender_CHOICES=(
        ('M','Male'),
        ('F','Female')

    )
    gender=models.CharField(
        max_length=1,
        choices=Gender_CHOICES,

    )

    phone=models.CharField(max_length=20,default='None')
    email=models.CharField(max_length=50,default="None")
    
    Level_CHOICES=(
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
        choices=Level_CHOICES,

    )

    Frequency_CHOICES=(
        (1,"Once/ week"),
        (2,"Twice/ week"),
        (3,"Three times/ week"),
        (4,"Four times/ week"),
        (5,"Five times/ week"),
        (6,"Six times/ week"),
        (7,"Everyday"),

    )

    frequency=models.IntegerField(
        choices=Frequency_CHOICES

    )

    Times_CHOICES=(
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

    times=models.CharField(max_length=3,choices=Times_CHOICES,default="None")

    def __str__(self):
        return self.first_name + " "+ self.last_name

