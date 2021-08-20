from django import forms


class LoginForm(forms.Form):
    name = forms.CharField(
        label='Student ID:',
        widget=forms.TextInput()
    )