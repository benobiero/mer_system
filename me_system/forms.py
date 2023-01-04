from django import forms
from .models import Grant,Comment


class GrantForm(forms.ModelForm):
    class Meta:
        model=Grant
        fields='__all__'
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields='__all__'


class MonthlyToolForm(forms.Form):
    
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
