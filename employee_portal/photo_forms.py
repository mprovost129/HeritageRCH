from django import forms
from catalog.models import Photo

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption', 'sort_order']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            existing_classes = widget.attrs.get("class", "").strip()
            if isinstance(widget, forms.ClearableFileInput):
                css_class = "form-control"
            elif isinstance(widget, forms.Textarea):
                css_class = "form-control"
            elif isinstance(widget, forms.Select):
                css_class = "form-select"
            else:
                css_class = "form-control"
            widget.attrs["class"] = f"{existing_classes} {css_class}".strip()
