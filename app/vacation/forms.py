from django.forms import EmailField, EmailInput, ModelForm, TextInput, CharField, PasswordInput
from .models import Comment
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    username = CharField(max_length=100, required=True, widget=TextInput(attrs={'class': 'form-control'}))    
    email = EmailField(widget=EmailInput(attrs={'class': 'form-control'}))
    password1 = CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    password2 = CharField(widget=PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 3:
            return username
        raise ValidationError('Имя пользователя должно быть больше 3-х символов')

    def clean_password2(self):
        pass1 = self.cleaned_data.get('password1')
        pass2 = self.cleaned_data.get('password2')
        if pass1 and pass2 and pass1 == pass2:
            return pass2
        raise ValidationError("Пароли не совпадают или пустые")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    