from django import forms
from .models import HoursWorked;


class LoginForm(forms.Form):
    name = forms.CharField(
        label='Student ID:',
        widget=forms.TextInput()
    )
    
class HoursWorkedForm(forms.ModelForm):

    
    def __init__(self, *args, **kwargs):
    
        super(HoursWorkedForm, self).__init__(*args, **kwargs)
        
        self.fields['newTimeIn'].required = False
        self.fields['newTimeOut'].required = False
        
        if self.instance.newTimeIn == None:
            self.initial['newTimeIn'] = self.instance.timeIn
        else:
            self.initial['newTimeIn'] = self.instance.newTimeIn

        if self.instance.newTimeOut == None:
            self.initial['newTimeOut'] = self.instance.timeOut
        else:
            self.initial['newTimeOut'] = self.instance.newTimeOut


    class Meta:
        model = HoursWorked
        fields = ('newTimeIn', 'newTimeOut')
        widgets = {
            'newTimeIn': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter time in here'
            }),
            'newTimeOut': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter time out here'
            })
        }
    
HoursWorkedFormSet = forms.modelformset_factory(HoursWorked, HoursWorkedForm, extra=1)