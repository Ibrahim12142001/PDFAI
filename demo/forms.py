from django import forms
from demo.models import CSVUpload

class CSVUploadForm(forms.ModelForm):
    class Meta:
        model = CSVUpload
        fields = ('csv_file',)