from django import forms
from django.forms import modelformset_factory
from django.contrib.auth.forms import AuthenticationForm

from dataschemas.models import DataSchema, DataColumn


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs["class"] = "form-control"


class DataSchemaForm(forms.ModelForm):
    class Meta:
        model = DataSchema
        fields = ["title"]
        widgets = {"title": forms.TextInput(attrs={"class": "form-control"})}


class DataColumnForm(forms.ModelForm):
    class Meta:
        model = DataColumn
        fields = ["title", "data_type", "range_from", "range_to", "order"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs["class"] = "form-control"

    def has_changed(self, *args, **kwargs):
        return True


DataColumnFormSet = modelformset_factory(
    DataColumn, DataColumnForm, min_num=1, extra=0, validate_min=1
)


class GenerateDataSetForm(forms.Form):
    schema = forms.IntegerField(widget=forms.HiddenInput())
    row_count = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs["class"] = "form-control"

    def clean_schema(self):
        schema = self.request.user.dataschemas.filter(
            id=self.cleaned_data["schema"]
        ).first()
        if not schema:
            raise forms.ValidationError("Invalid dataschema")
        return schema
