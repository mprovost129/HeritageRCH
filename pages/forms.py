# ──────────────────────────────────────────────────────────────────────────────
# pages/forms.py (Lead form)
# ──────────────────────────────────────────────────────────────────────────────
from django import forms

class LeadForm(forms.Form):
    name = forms.CharField(max_length=160)
    email = forms.EmailField()
    phone = forms.CharField(max_length=40, required=False)
    message = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            existing_classes = widget.attrs.get("class", "").strip()
            if isinstance(widget, forms.Textarea):
                css_class = "form-control"
                widget.attrs.setdefault("rows", 5)
            else:
                css_class = "form-control"
            widget.attrs["class"] = f"{existing_classes} {css_class}".strip()
