from django import forms
from .models import Expense
from datetime import date


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'date', 'description', 'amount']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # Date picker
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ Set the default value for the date field
        self.fields['date'].initial = date.today().strftime('%Y-%m-%d')
