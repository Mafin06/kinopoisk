from django import forms
from .models import Contact
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField()
    
    class Meta:
        model = Contact
        fields = ("email",)
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "editContent",
                "placeholder": "Ваш E-mail ...",
                "required": True
            })
        }