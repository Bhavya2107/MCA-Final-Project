from django import forms


class InquiryForm(forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    phone = forms.CharField(max_length=30, required=False)
    message = forms.CharField(widget=forms.Textarea)
    product = forms.CharField(required=False)
