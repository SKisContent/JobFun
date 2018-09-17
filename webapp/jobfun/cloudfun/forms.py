from django import forms

class WordCloudForm(forms.Form):
    urls = forms.CharField(widget=forms.Textarea)

