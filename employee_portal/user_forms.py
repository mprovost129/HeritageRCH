
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            existing_classes = widget.attrs.get("class", "").strip()
            if isinstance(widget, forms.CheckboxInput):
                css_class = "form-check-input"
            elif isinstance(widget, forms.Select):
                css_class = "form-select"
            elif isinstance(widget, forms.Textarea):
                css_class = "form-control"
                widget.attrs.setdefault("rows", 4)
            else:
                css_class = "form-control"
            widget.attrs["class"] = f"{existing_classes} {css_class}".strip()

    def save(self, commit=True):
        user = super().save(commit=False)
        pwd = self.cleaned_data.get('password')
        if pwd:
            user.set_password(pwd)
        if commit:
            user.save()
        return user
