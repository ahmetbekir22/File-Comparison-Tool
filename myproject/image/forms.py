from django import forms

class ImageUploadForm(forms.Form):
    image1 = forms.ImageField(label='Image 1')
    image2 = forms.ImageField(label='Image 2')
