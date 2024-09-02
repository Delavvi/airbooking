from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import AuthenticationForm
from .models import MyUser


class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = MyUser
        fields = ['username', 'password', 'password2', 'email']
        widgets = {'email': forms.TextInput(attrs={'class': 'form-control', 'id': 'email'}),
                   'password2': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password2'}),
                   'password': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password1'})}

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        if MyUser.objects.filter(email=cleaned_data.get('email')).exists():
            raise ValidationError("Taken Email")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = 'register'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Submit'))


class SignForm(AuthenticationForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = kwargs.pop('request', None)
        self.helper = FormHelper()
        self.helper.form_tag = 'sign'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Submit'))