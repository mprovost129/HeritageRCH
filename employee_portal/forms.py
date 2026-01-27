from django import forms
from catalog.models import Community, FloorPlan, AvailableHome

class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = '__all__'

class FloorPlanForm(forms.ModelForm):
    class Meta:
        model = FloorPlan
        fields = '__all__'

class AvailableHomeForm(forms.ModelForm):
    class Meta:
        model = AvailableHome
        fields = '__all__'
