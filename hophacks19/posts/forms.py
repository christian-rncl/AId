from django import forms
from . import models


class PostForm(forms.ModelForm):
    class Meta:
        fields = ["message", "amount", "disaster"]
        model = models.Post

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["disaster"].queryset = models.Disaster.objects.all()

