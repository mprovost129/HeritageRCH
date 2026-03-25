from django import forms
from catalog.models import Community, FloorPlan, AvailableHome
import json
from django.core.exceptions import ValidationError


def apply_bootstrap_classes(form):
    for field in form.fields.values():
        widget = field.widget
        existing_classes = widget.attrs.get("class", "").strip()
        if isinstance(widget, forms.CheckboxInput):
            css_class = "form-check-input"
        elif isinstance(widget, forms.SelectMultiple):
            css_class = "form-select"
            widget.attrs.setdefault("size", 6)
        elif isinstance(widget, forms.Select):
            css_class = "form-select"
        elif isinstance(widget, forms.Textarea):
            css_class = "form-control"
            widget.attrs.setdefault("rows", 4)
        else:
            css_class = "form-control"
        widget.attrs["class"] = f"{existing_classes} {css_class}".strip()


def normalize_info_sections(raw_value, label):
    if not raw_value:
        return []
    try:
        parsed = json.loads(raw_value)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{label} sections must be valid JSON.") from exc
    if not isinstance(parsed, list):
        raise ValidationError(f"{label} sections must be a list of section objects.")

    normalized_sections = []
    for section in parsed:
        if not isinstance(section, dict):
            continue
        header = str(section.get("header", "")).strip()
        items = section.get("items", [])
        if not isinstance(items, list):
            items = []

        normalized_items = []
        for item in items:
            if not isinstance(item, dict):
                continue
            key = str(item.get("key", "")).strip()
            value = str(item.get("value", "")).strip()
            if key or value:
                normalized_items.append({"key": key, "value": value})

        if header or normalized_items:
            normalized_sections.append({"header": header, "items": normalized_items})
    return normalized_sections


class CommunityForm(forms.ModelForm):
    info_sections = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Community
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_sections = self.instance.info_sections if self.instance and self.instance.pk else []
        self.fields["info_sections"].initial = json.dumps(current_sections or [])
        apply_bootstrap_classes(self)

    def clean_info_sections(self):
        return normalize_info_sections(self.cleaned_data.get("info_sections", ""), "Community")

class FloorPlanForm(forms.ModelForm):
    info_sections = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = FloorPlan
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_sections = self.instance.info_sections if self.instance and self.instance.pk else []
        self.fields["info_sections"].initial = json.dumps(current_sections or [])
        apply_bootstrap_classes(self)

    def clean_info_sections(self):
        return normalize_info_sections(self.cleaned_data.get("info_sections", ""), "Plan")


class AvailableHomeForm(forms.ModelForm):
    info_sections = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = AvailableHome
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_sections = self.instance.info_sections if self.instance and self.instance.pk else []
        self.fields["info_sections"].initial = json.dumps(current_sections or [])
        apply_bootstrap_classes(self)

    def clean_info_sections(self):
        return normalize_info_sections(self.cleaned_data.get("info_sections", ""), "Home")
