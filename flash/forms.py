from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Movie
import pdb

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='ユーザーの名前')
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード',widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='パスワードの確認', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'username']

        def clean_confirm_password(self):
            cd = self.cleaned_data
            if cd['password'] != cd['confirm_password']:
                raise forms.ValidationError('パスワードが一致しません')
            
            return cd['confirm_password']

class MovieForm(forms.ModelForm):
    movie = forms.FileField(label='変換したい動画')

    class Meta:
        model = Movie
        fields = ['movie']
        widget = forms.FileInput(attrs={'id':'movie_id'})
