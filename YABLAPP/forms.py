from django import forms
from .models import Book, Grading
from django.contrib.auth.models import User


forms.DateInput.input_type="date"
class searchBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title',)
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class GradingForm(forms.ModelForm):
    vsbh = forms.IntegerField(min_value=0,max_value=100,widget=forms.NumberInput(attrs={'type':'range', 'step': '1'}))

    class Meta:
        model = Grading
        fields = (  'roman', 'pos', 'real', 'span', 'vsbh')
