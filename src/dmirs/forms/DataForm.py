from django import forms
from django.core.exceptions import ValidationError


class DataForm(forms.Form):
    tenements = forms.JSONField()
    start_date = forms.DateField(input_formats=['%d-%m-%Y'])
    end_date = forms.DateField(input_formats=['%d-%m-%Y'])

    def clean_tenements(self):
        tenements = self.cleaned_data['tenements']

        # Ensure tenements is a list
        if not isinstance(tenements, list):
            raise forms.ValidationError('Tenements must be an array.')

        # You can add additional validation for the elements in the array if needed

        return tenements

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and start_date >= end_date:
            raise ValidationError("Start date must be older than end date.")
