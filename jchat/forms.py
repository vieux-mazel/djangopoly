from django import forms
from .models import Spy_code, Room
from monopoly.models import Player
class SpyForm(forms.Form):
    spycode = forms.CharField(label='Spy Code', max_length=10)

class SpyTeamSelector(forms.Form):
    spyteam = forms.ModelChoiceField(label='Equipe', queryset=Room.objects.all(), empty_label=None)

# place form definition here
