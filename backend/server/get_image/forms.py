from django import forms

class ImageForm(forms.Form):
    image   = forms.ImageField()
#    comment = forms.CharField(max_length=255)
#    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))


