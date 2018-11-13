# pdf/models.py
from django import forms


class PdfExtractForm(forms.Form):
    file = forms.FileField(label="Upload PDF Document")
    page = forms.CharField(max_length=20, label="Page Number")

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file.name.lower().endswith('.pdf'):
            raise forms.ValidationError("Only pdf documents are allowed. ")
        return file


class PdfMergeForm(forms.Form):
    file1 = forms.FileField(label="PDF file 1")
    file2 = forms.FileField(label="PDF file 2", required=False)
    file3 = forms.FileField(label="PDF file 3", required=False)
    file4 = forms.FileField(label="PDF file 4", required=False)
    file5 = forms.FileField(label="PDF file 5", required=False)


class PdfReplaceForm(forms.Form):
    file1 = forms.FileField(label="Replacement page")
    file2 = forms.FileField(label="PDF document to be replaced")
    page = forms.IntegerField(label="Replace page number")



