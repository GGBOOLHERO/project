from django import forms

class SellerForm(forms.Form):
	username = forms.CharField(required=True, error_messages={'required': '必填!'})
	password = forms.CharField(required=True, min_length=6, error_messages={'required': '必填!', 'min_length':'长度至少为6位'})
	email = forms.EmailField(required=True, error_messages={'required': '必填!'})
	phone = forms.CharField(required=True, error_messages={'required': '必填!'})
	address = forms.CharField(required=True, error_messages={'required': '必填!'})
	gender = forms.CharField(required=True)
	headimg = forms.ImageField(required=True, error_messages={'required': '必选!'})