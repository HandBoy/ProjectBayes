from django import forms

from core.models import BaysianNet, Competence, Variable


class BaysianForm(forms.ModelForm):
    class Meta:
        model = BaysianNet
        fields = '__all__'


class CompetenceForm(forms.ModelForm):
    class Meta:
        model = Competence
        fields = '__all__'

class VariableForm(forms.ModelForm):
    class Meta:
        model = Variable
        fields = '__all__'