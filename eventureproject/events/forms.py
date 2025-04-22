from django import forms
from .models import Events

class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['name', 'description', 'start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'px-3 py-2 border border-gray-400 rounded-md w-full'}),
            'description': forms.Textarea(attrs={'class': 'px-3 py-2 border border-gray-400 rounded-md w-full'}),
            'start_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'px-3 py-2 border border-gray-400 rounded-md w-full'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'px-3 py-2 border border-gray-400 rounded-md w-full'
            }),

        }
