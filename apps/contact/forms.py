from django import forms

from .models import ContactSubmission


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ["name", "email", "phone", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }
