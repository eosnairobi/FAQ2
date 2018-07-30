from django import forms
from .models import SuggestedTool


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = SuggestedTool
        fields ='__all__'
        exclude = ('id',)