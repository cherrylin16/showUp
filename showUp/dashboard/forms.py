from django import forms
from .models import EventPost
from datetime import date, datetime

class EventPostForm(forms.ModelForm):
    caterer_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}))
    caterer_phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123-456-7890', 'pattern': '[0-9]{3}-[0-9]{3}-[0-9]{4}'}))
    caterer_address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street, City, State, Zip'}))
    
    catering_budget = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.00, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}))
    supplies_budget = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.00, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}))

    class Meta:
        model = EventPost
        # Only include fields that actually exist in your 'Events' SQL table here
        fields = ['event_name', 'date', 'time', 'event_description', 'location'] 
        
        widgets = {
            'date': forms.DateInput(attrs={'class':'form-control', 'type': 'date', 'required': True}),
            'time': forms.TimeInput(attrs={'class':'form-control', 'type': 'date', 'required': True}),
            'event_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of Event', 'required': True}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Location', 'required': True}),
            'event_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Event Description'}),
        }
        
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['date'].widget.attrs['min'] = date.today().isoformat()
    
    # def clean_date(self):
    #     selected_date = self.cleaned_data['date']
    #     if isinstance(selected_date, str):
    #         selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    #     if selected_date < date.today():
    #         raise forms.ValidationError("Trip date cannot be in the past.")
    #     return selected_date
    
    
from .models import EventPost, EventPhoto

class EventPhotoForm(forms.ModelForm):
    image_file = forms.ImageField(required=True)

    class Meta:
        model = EventPhoto
        fields = []

    def save(self, commit=True):
        photo = super().save(commit=False)
        uploaded_file = self.cleaned_data["image_file"]
        photo.image = uploaded_file.read()

        if commit:
            photo.save()

        return photo