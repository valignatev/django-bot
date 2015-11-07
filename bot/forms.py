from django import forms

from .models import Human, Bot


class HumanForm(forms.ModelForm):

    class Meta:
        model = Human
        fields = ('username',)


class BotForm(forms.ModelForm):

    class Meta:
        model = Bot
        fields = ('command',)

