# from django import forms
# from dashboard.models import Admin


# admin = Admin.objects.all()
# class LoginFrom(forms.ModelForm):
#     email = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         fields = ['email', 'password']

#     def clean(self):
#         email = self.cleaned_data.get('email')
#         password = self.cleaned_data.get('password')

#         erroremail = forms.ValidationError({
#             'email' : 'Email didn\'t match.'
#         })

#         errorpassword = forms.ValidationError({
#             'password' : 'Password did\'t match.'
#         })

#         user_queryset = admin.objects.filter(email=email)
#         if not user_queryset.exists():
#             raise erroremail

#         user = user_queryset.first()
#         if not user.check_password(password):
#             raise errorpassword
        
#         self.instance = user