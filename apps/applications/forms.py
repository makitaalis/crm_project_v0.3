from django import forms
from .models import Application, Status


class ApplicationForm(forms.ModelForm):
    status_comment = forms.CharField(
        label='Комментарий к изменению статуса',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )

    class Meta:
        model = Application
        fields = ['client', 'operator', 'status', 'categories', 'notes', 'recall_date']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'operator': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'recall_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


class ApplicationOperatorForm(forms.ModelForm):
    status_comment = forms.CharField(
        label='Комментарий',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )

    class Meta:
        model = Application
        fields = ['status', 'notes', 'recall_date']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'recall_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }