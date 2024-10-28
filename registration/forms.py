from django import forms
from .models import Registrant
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class RegistrantForm(forms.ModelForm):
    class Meta:
        model = Registrant
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'state', 'country', 'accommodation', 'marital_status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))
