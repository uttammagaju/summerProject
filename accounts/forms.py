# from socket import fromshare
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)

    class Meta:
        fields = ['email', 'password']

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        error = forms.ValidationError({
            'email' : 'Email or Password didn\'t match.'
        })

        user_queryset = User.objects.filter(email=email)
        if not user_queryset.exists():
            raise error

        user = user_queryset.first()
        if not user.check_password(password):
            raise error
        
        self.instance = user