from django import forms
from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _

from .models import Project


class ProjectForm(forms.ModelForm):
    """
    This form is used to create and edit Project instances. It uses Django's ModelForm functionality
    to generate fields based on the Project model's fields.
    """
    title = forms.CharField(max_length=200, label='Tytuł')
    description = forms.CharField(widget=forms.Textarea, label='Krótki opis')

    class Meta:
        """
        Meta class defining the model and fields to be used by the form.
        """
        model = Project
        fields = ['title', 'description']

    def __init__(self, *args, **kwargs):
        """
        Initialize the form. Also, add a custom class 'input' to every field in the form.
        """
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
