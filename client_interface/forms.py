from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from authentication.models import Passenger


class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['name', 'sur_name', 'gender']


