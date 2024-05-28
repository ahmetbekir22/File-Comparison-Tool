
from django import forms

class UploadFileForm(forms.Form):
    file1 = forms.FileField(label='File 1')
    file2 = forms.FileField(label='File 2')
