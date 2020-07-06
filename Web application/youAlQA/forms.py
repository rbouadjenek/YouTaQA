from django import forms

class searchForm(forms.Form):
    question = forms.CharField(label='', max_length=100,widget=forms.TextInput(attrs={'class':'form-control','id':'search_qst_bar','placeholder':'Ask your question here','name':'question'}),disabled=False)