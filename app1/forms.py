from django import forms

class AddDocumentForm(forms.Form):
    database_name = forms.CharField(label='Database Name', max_length=100)
    collection_name = forms.CharField(label='Collection Name', max_length=100)
    document_data = forms.CharField(label='Document Data (JSON)', widget=forms.Textarea)

class DocumentSelectionForm(forms.Form):
    database_name = forms.CharField(label='Database Name', max_length=100)
    collection_name = forms.CharField(label='Collection Name', max_length=100)

class EditDocumentForm(forms.Form):
    document_id = forms.CharField(label='Document ID', widget=forms.HiddenInput())
    document_data = forms.CharField(label='Document Data (JSON)', widget=forms.Textarea())