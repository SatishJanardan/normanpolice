from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

GRAPHCHOICES = ('Incidents vs Cases Frequency (in minutes)',
	'Incident Type Frequency (sorted by frequency)',
	'Incident Type Urgency (sorted by frequency)',
	'Graph D',
	'Graph E',
	'Graph F',
	'Graph G',
	'Graph H',
	'Graph I',
	'Graph J')

class GraphTypeForm(forms.Form):
	graph_selection = forms.ChoiceField(choices=GRAPHCHOICES)
	start_date = forms.DateField(help_text="Enter a starting date in June 2020.")
	end_date = forms.DateField(help_text="Enter an ending date in June 2020.")
	incident_urgency = forms.IntegerField(help_text="Enter a urgency (between 0 and 5, 6 implies all).")


	def clean_start_date(self):
		data = self.cleaned_data['start_date']
		
		# Check if a date is not in the past. 
		if data < datetime.date(2020, 6, 1):
			raise ValidationError(_('Invalid date - not a date in june'))

		# Check if a date is in the allowed range (+4 weeks from today).
		if data > datetime.date(2020, 6, 25):
			raise ValidationError(_('Invalid date - not a date before 6/25/2020'))

		# Remember to always return the cleaned data.
		return data

	def clean_end_date(self):
		data = self.cleaned_data['end_date']
		
		# Check if a date is not in the past. 
		if data < datetime.date(2020, 6, 1):
			raise ValidationError(_('Invalid date - not a date in june'))

		# Check if a date is in the allowed range (+4 weeks from today).
		if data > datetime.date(2020, 6, 25):
			raise ValidationError(_('Invalid date - not a date before 6/25/2020'))

		# Remember to always return the cleaned data.
		return data

	def clean_incident_urgency(self):
		data = self.cleaned_data['incident_urgency']
		
		# Check if a date is not in the past. 
		if data < 0 or data > 6:
			raise ValidationError(_('Invalid Urgency ranking is between 0 and 5'))

		# Remember to always return the cleaned data.
		return data

