from django import forms

class TextInputForm(forms.Form):
    input_text = forms.CharField(widget=forms.Textarea, label='Metin Girin')
