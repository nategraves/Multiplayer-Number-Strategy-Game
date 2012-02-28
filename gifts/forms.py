from django import forms

from giftalink.gifts.models import Gift

class GiftForm(forms.ModelForm):
	
	gift_to = forms.CharField(
				widget=forms.TextInput(attrs={'class':'input-xlarge span4'}))
	gift_from = forms.CharField(
				widget=forms.TextInput(attrs={'class':'input-xlarge span4'}))
	url = forms.CharField(
				widget=forms.TextInput(attrs={'class':'input-xlarge span4'}))
	message = forms.CharField(
				required=False, widget=forms.Textarea(attrs={'class':'input-xlarge span4'}))

	class Meta:
		model = Gift
		fields = ('gift_to', 'gift_from', 'url', 'message',)