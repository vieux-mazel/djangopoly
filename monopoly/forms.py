from django import forms
from .models import Spy_code
from monopoly.models import Player
class BuildHouseForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.square_id = kwargs.pop('square_id')
        super(BuildHouseForm,self).__init__(*args,**kwargs)
        self.fields['square_id'].widget = forms.forms.CharField(value=square_id ,widget=forms.HiddenInput())

class BuildOtherForm(forms.Form):
    spyteam = forms.ModelChoiceField(label='Equipe', queryset=Player.objects.all(), empty_label=None)

# place form definition here
