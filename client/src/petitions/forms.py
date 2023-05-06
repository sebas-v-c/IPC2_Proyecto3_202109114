from django import forms


class XmlForm(forms.Form):
    xml_file = forms.FileField(
        label="Select an XML file",
        help_text="max. 42 megabytes",
        widget=forms.ClearableFileInput(attrs={"multiple": False}),
    )
