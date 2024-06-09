from django import forms
from .models import Customer, CustomerDocument

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['surname', 'firstname', 'nationality', 'gender']

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = CustomerDocument
        fields = ['attached_file']
