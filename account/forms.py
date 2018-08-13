from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    def __init__(self):
        super(UserForm, self).__init__()
        self.fields.get('username').help_text = None
        self.fields.get('username').required = True
        self.fields.get('password').required = True
        self.fields.get('email').required = True

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        widgets = {'password': forms.PasswordInput()}
