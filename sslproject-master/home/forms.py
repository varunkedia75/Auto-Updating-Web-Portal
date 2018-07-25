from django import forms
from fpagecse.models import Faculty
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


# class MyFacultyForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#
#     class Meta:
#         model = Faculty
#         fields = ['faculty_name', 'department', 'designation', 'phone', 'email', 'room_no']


class UserForm(forms.ModelForm):
        password = forms.CharField(widget=forms.PasswordInput)
        confirm_password = forms.CharField(widget=forms.PasswordInput)
        captcha = CaptchaField()

        class Meta:
            model = User
            fields = ['username', 'email', 'password']

        def clean(self):
            cleaned_data = super(UserForm, self).clean()
            password = cleaned_data.get("password")
            confirm_password = cleaned_data.get("confirm_password")

            if password != confirm_password:
                raise forms.ValidationError(
                    "Password and Confirm Password does not match"
                )

        # def __init__(self, *args, **kwargs):
        #     super(UserForm, self).__init__(*args, **kwargs)
        #     self.fields['username'].widget.attrs['placeholder'] = _('Enter your username')

# class LoginForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     class Meta:
#         model = Faculty
#         fields = ['username', 'password']







