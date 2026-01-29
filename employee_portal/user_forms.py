
from django import forms
from accounts.models import CustomUser

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank to keep unchanged.")
    class Meta:
        model = CustomUser
        fields = [
            'email', 'first_name', 'last_name', 'picture', 'phone_number_1', 'phone_number_2',
            'address_1', 'address_2', 'city', 'state', 'zip_code',
            'role', 'company_role', 'bio',
            'is_staff', 'is_superuser', 'is_active', 'password'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        pwd = self.cleaned_data.get('password')
        if pwd:
            user.set_password(pwd)
        if commit:
            user.save()
        return user
