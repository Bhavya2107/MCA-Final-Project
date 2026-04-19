from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    phone = forms.CharField(max_length=30, required=False)
    message = forms.CharField(widget=forms.Textarea)
    # Optional product the user is enquiring about. Filled from product pages using a query param.
    product = forms.CharField(max_length=200, required=False, widget=forms.HiddenInput())
