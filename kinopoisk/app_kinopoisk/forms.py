from django import forms

from .models import Reviews, Rating, RatingStar

class ReviewForm(forms.ModelForm):
    '''форма отзывов'''
    class Meta:
        model = Reviews
        fields = ("name", "text", "email")

class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None)
    class Meta:
        model = Rating
        fields = ('star', )