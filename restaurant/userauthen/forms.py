from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser
from restrecommender.models import Restaurantdata


def unique_values():
    return Restaurantdata.objects.values_list('city', 'city').distinct()


class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=100, help_text=' ')

    locality = forms.ChoiceField(
        required=False,
        choices=unique_values,
        widget=forms.Select,
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'username', 'email',
                  'locality', 'password1', 'password2']
