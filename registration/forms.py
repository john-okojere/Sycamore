from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Registrant, InHouse

# Registrant Form
class RegistrantForm(forms.ModelForm):
    class Meta:
        model = Registrant
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'address',
            'state',
            'country',
            'accommodation',
            'marital_status'
        ]
        widgets = {
            'accommodation': forms.RadioSelect(choices=[
                ('yes', 'Yes'),
                ('no', 'No')
            ]),
            'marital_status': forms.Select(choices=[
                ('single', 'Single'),
                ('married', 'Married'),
                ('divorced', 'Divorced'),
                ('widowed', 'Widowed')
            ]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))

# InHouse Form
class InHouseForm(forms.ModelForm):
    class Meta:
        model = InHouse
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'department'
        ]
        widgets = {
            'department': forms.Select(choices=[
                ('ushering', 'Ushering'),
                ('sanctuary', 'Sanctuary'),
                ('spirit & Truth', 'Spirit & Truth'),
                ('technical', 'Technical'),
                ('light and Power', 'Light & Power'),
                ('media', 'New Wine Media'),
                ('follow up', 'Labour Room (follow_up)'),
                ('decoration', 'Decoration'),
                ('welfare', 'Taste & See'),
                ('pastoral', 'Pastoral Care'),
            ])
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))

# Optional: Volunteer Confirmation Form (if needed)
class VolunteerForm(forms.Form):
    volunteer = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
