from django import forms
from django.contrib.auth import get_user_model
from leads.models import Agent
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class AgentModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name'
        )