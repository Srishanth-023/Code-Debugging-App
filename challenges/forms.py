from django import forms
from .models import Week, Challenge

class WeekForm(forms.ModelForm):
    class Meta:
        model = Week
        fields = ['week_number', 'title', 'description', 'start_date', 'end_date', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError("End date must be after start date.")
        
        return cleaned_data

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['week', 'title', 'description', 'buggy_code', 'expected_output', 'difficulty', 'points', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'buggy_code': forms.Textarea(attrs={'rows': 10, 'class': 'code-editor'}),
            'expected_output': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['week'].queryset = Week.objects.all().order_by('-week_number')
        
        # Set default order to next available number
        if not self.instance.pk:
            week_id = self.data.get('week') or self.initial.get('week')
            if week_id:
                try:
                    week = Week.objects.get(id=week_id)
                    next_order = week.challenges.count() + 1
                    self.fields['order'].initial = next_order
                except Week.DoesNotExist:
                    pass