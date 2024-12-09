from django import forms
from .models import Garden, Plot, Plant,User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class GardenForm(forms.ModelForm):
    class Meta:
        model = Garden
        fields = ['name', 'location', 'user']
class PlotForm(forms.ModelForm):
    class Meta:
        model = Plot
        fields = ['name', 'days_since_watered']
        labels = {
            'days_since_watered': 'Days Since Last Watering'
        }
        
        
class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'days_since_planted', 'days_until_mature', 'description', 'plot']
        labels = {
            'days_since_planted': 'Days Since Planted',
            'days_until_mature': 'Days Until Mature'
        }




