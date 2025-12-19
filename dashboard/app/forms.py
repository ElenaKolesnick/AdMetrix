from django import forms
from .models import UserProfile
from django.contrib.auth.models import User

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="Электронная почта", required=False)

    class Meta:
        model = UserProfile
        fields = ['full_name', 'company_name', 'phone', 'about', 'avatar']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.required = False