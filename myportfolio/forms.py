from django import forms
from .models import Intro

class IntroForm(forms.ModelForm):
    class Meta:
        model = Intro
        fields = [
            'full_name', 'profile_picture', 'tagline', 'about_me',
            'location', 'email', 'phone', 'linkedin', 'github',
            'twitter', 'website', 'resume'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add form-control class to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-input',
                'id': f'id_{field}'
            })

        # Customize specific fields
        self.fields['full_name'].widget.attrs.update({
            'placeholder': 'Enter your full name',
            'required': True
        })
        self.fields['profile_picture'].widget.attrs.update({
            'class': 'hidden-input',
            'accept': 'image/*'
        })
        self.fields['about_me'].widget = forms.Textarea(attrs={
            'rows': 5,
            'class': 'form-input',
            'placeholder': 'Write a brief introduction about yourself'
        })

    def clean(self):
        cleaned_data = super().clean()
        # Print form data for debugging
        print("Form Data:", self.data)
        print("Files:", self.files)
        return cleaned_data