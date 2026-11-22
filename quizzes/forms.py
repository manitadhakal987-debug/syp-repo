from django import forms
from .models import HairProfile

CONCERN_OPTIONS = [
    ('frizz', 'Excessive Frizz & Flyaways (especially during Nepal monsoons)'),
    ('dryness', 'Dryness & Lack of Moisture'),
    ('breakage', 'Strand Breakage & Split Ends'),
    ('dandruff', 'Scalp Flakes & Itchiness'),
    ('lack_of_volume', 'Flat Roots / Lack of Volume'),
    ('heat_damage', 'Past Heat Straightening or Chemical Damage'),
]

class CurlProfileQuizForm(forms.ModelForm):
    concerns = forms.MultipleChoiceField(
        choices=CONCERN_OPTIONS,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True,
        help_text="Select all concerns that apply to your hair."
    )

    class Meta:
        model = HairProfile
        fields = ['curl_type', 'porosity', 'density', 'scalp_type', 'concerns', 'budget']
        widgets = {
            'curl_type': forms.RadioSelect(attrs={'class': 'btn-check'}),
            'porosity': forms.RadioSelect(attrs={'class': 'btn-check'}),
            'density': forms.RadioSelect(attrs={'class': 'btn-check'}),
            'scalp_type': forms.RadioSelect(attrs={'class': 'btn-check'}),
            'budget': forms.RadioSelect(attrs={'class': 'btn-check'}),
        }

    def clean_concerns(self):
        concerns_list = self.cleaned_data.get('concerns', [])
        return ",".join(concerns_list)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.concerns:
            self.initial['concerns'] = self.instance.concerns_list
