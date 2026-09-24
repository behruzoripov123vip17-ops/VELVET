from django import forms
from .models import UserProfile


class AvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("avatar",)
        widgets = {
            "avatar": forms.ClearableFileInput(attrs={
                "accept": "image/*",
                "class": "form-control",
            })
        }
