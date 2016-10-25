from django import forms
from django.forms import ModelForm
import csv
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from app.models import Test_Suite, Set_Top_Box, Revo, racktestresult


class BootstrapAuthenticationForm(AuthenticationForm):
    
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   "class": "form-control",
                                   "placeholder": "User name"}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   "class": "form-control",
                                   "placeholder":"Password"}))


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password")


class NameForm(forms.Form):
    print "I am in forms"


#     class Meta:
#         model = racktestresult
#         widgets = {
#             'Date': forms.DateInput(attrs={'class':'datepicker'}),
#         }