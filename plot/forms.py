from django import forms

CHOICES = (
    ('square', 'Square'),
    ('circle', 'Circle'),
    )
class DataForm(forms.Form):
    f = forms.DecimalField(min_value=0.01, max_value=50, max_digits=9,
            widget=forms.TextInput(attrs={'size':'5'}), )
    xran = forms.DecimalField(min_value=0, max_value=5000,
            widget=forms.TextInput(attrs={'size':'5'}), )
    size = forms.DecimalField(min_value=0, max_value=100,
            widget=forms.TextInput(attrs={'size':'5'}), )
    shape = forms.ChoiceField(choices=CHOICES, initial="square",
            widget=forms.RadioSelect)
