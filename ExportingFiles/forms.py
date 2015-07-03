from django import forms
from .models import Weather, Town


class WeatherForm(forms.ModelForm):
    town = forms.ModelChoiceField(
        queryset=Town.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Weather
        fields = ['town']
