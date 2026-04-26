from django import forms
from .models import EventPost
from datetime import date, datetime

class EventPostForm(forms.ModelForm):
    catering_budget = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.00)
    supplies_budget = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.00)

    class Meta:
        model = EventPost
        # 'location_snum', 'location_street', 'location_city' 'location_state', 'location_zip,
        fields = ['host_name','event_name', 'date', 'start_time', 'end_time', 'location', 'caterer_address', 'caterer_phone', 'caterer_name', 'catering_budget', 'supplies_budget', 'event_description', 'image', 'image_visibility']
        widgets = {
            'host_name': forms.TextInput(attrs={'class': 'form-control', 'rows':1, 'placeholder': 'Host Name', 'required': True}),
            'event_name': forms.TextInput(attrs={'class': 'form-control', 'rows':1, 'placeholder': 'Name of Event', 'required': True}),
            'date': forms.DateInput(attrs={'class':'form-control', 'type': 'date', 'required': True}),
            'start_time': forms.TimeInput(attrs={'class':'form-control', 'type': 'time', 'required': True}),
            'end_time': forms.TimeInput(attrs={'class':'form-control', 'type': 'time', 'required': True}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Street, City, State, Zip Code', 'required': True}),
            'caterer_address': forms.TextInput(attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Street, City, State, Zip Code', 'required': True}),
            'caterer_phone': forms.TextInput(attrs={
                    'class': 'form-control', 
                    'placeholder': '123-456-7890',
                    'pattern': '[0-9]{3}-[0-9]{3}-[0-9]{4}'
            }),
            'caterer_name': forms.TextInput(attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Company Name'}),
            'event_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Create a description for your event'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'image_visibility': forms.Select(attrs={'class': 'form-control'}),
        }
        
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['min'] = date.today().isoformat()
    
    # def clean_date(self):
    #     selected_date = self.cleaned_data['date']
    #     if isinstance(selected_date, str):
    #         selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    #     if selected_date < date.today():
    #         raise forms.ValidationError("Trip date cannot be in the past.")
    #     return selected_date