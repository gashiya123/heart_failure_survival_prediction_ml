
from django import forms


class DoctorLoginForm(forms.Form):
    username=forms.CharField(max_length=100)
    password=forms.CharField(widget=forms.PasswordInput)


class AdminLoginForm(forms.Form):
    username=forms.CharField(max_length=150)
    password=forms.CharField(widget=forms.PasswordInput)


class DoctorForm(forms.Form):
    name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8
    )


class PatientForm(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField(min_value=1, max_value=120)
    sex = forms.ChoiceField(
        choices=[
            ("1", "Male"),
            ("0", "Female"),
        ]
    )
    contact = forms.CharField(max_length=20)

