from django import forms
from .models import NewCLIChallenge as Challenge
class CLIChallengeForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter challenge title',
            'class': 'form-control'
        })
    )
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'Describe the challenge in detail...',
            'class': 'form-control',
            'rows': 5
        })
    )
    category = forms.ChoiceField(
        choices=Challenge.CATEGORY_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    difficulty = forms.ChoiceField(
        choices=Challenge.DIFFICULTY_LEVELS,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    class Meta:
        model = Challenge
        fields = ('title', 'description', 'category', 'difficulty')