
from django import forms
from .models import Test


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = [
            'departement',
            'date',
        ]

    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control validate'})
        self.fields['date'].widget.input_type = 'date'
