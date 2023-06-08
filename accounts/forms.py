from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        error_message = "Email or password is incorrect."

        user_queryset = User.objects.filter(email=email)
        if not user_queryset.exists():
            raise forms.ValidationError(error_message)

        user = user_queryset.first()
        if not user.check_password(password):
            raise forms.ValidationError(error_message)

        self.instance = user
