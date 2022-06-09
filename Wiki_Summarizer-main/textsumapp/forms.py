from django import forms

class urlform(forms.Form):
    url=forms.URLField(max_length=500)
    percentage = forms.ChoiceField(choices=(
    
    (10, "10%"),
    (20, "20%"),
    (30, "30%"),
    (40,"40%"),
    (50,"50%")
))