# ──────────────────────────────────────────────────────────────────────────────
# pages/forms.py (Lead form)
# ──────────────────────────────────────────────────────────────────────────────
from django import forms

class LeadForm(forms.Form):
    name = forms.CharField(max_length=160)
    email = forms.EmailField()
    phone = forms.CharField(max_length=40, required=False)
    message = forms.CharField(widget=forms.Textarea, required=False)