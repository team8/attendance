from django import forms
class SubteamForm(forms.Form):
	subteam_name = forms.CharField(label = "lol", max_length = 100)