from django import forms

class NameForm(forms.Form):
    first_name = forms.CharField(label='first name', max_length=100)