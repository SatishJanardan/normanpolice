from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
from police.models import Graphdata, Cat, Crime, OffenseCat, Officer, Arrest, Case, Weather
#from .models import Post

class GraphTypeForm(forms.ModelForm):
	class Meta:
		model = Graphdata
		fields = ('bucket_Size', 'start_Date', 'end_Date', 'start_Urgency', 'end_Urgency',)

	def clean_bucket(self):
		data = self.cleaned_data['bucket_Size']
		
		if data < 0:
			raise ValidationError(_('Invalid Bucket size must greater than 0'))

		if data > 1440:
			raise ValidationError(_('Invalid Bucket size must less than 1440'))

		# Remember to always return the cleaned data.
		return data

	def clean_start_date(self):
		data = self.cleaned_data['start_Date']
		
		# Check if a date is not in the past. 
		if data < datetime.date(2020, 6, 1):
			raise ValidationError(_('Invalid date - not a date after 6/1/2020'))

		# Check if a date is in the allowed range (+4 weeks from today).
		if data > datetime.date(2020, 7, 9):
			raise ValidationError(_('Invalid date - not a date before 7/9/2020'))

		# Remember to always return the cleaned data.
		return data

	def clean_end_date(self):
		data = self.cleaned_data['end_Date']
		data2 = self.cleaned_data['start_Date']
		
		# Check if a date is not in the past. 
		if data < datetime.date(2020, 6, 1):
			raise ValidationError(_('Invalid date - not a date after 6/1/2020'))

		# Check if a date is in the allowed range.
		if data > datetime.date(2020, 7, 9):
			raise ValidationError(_('Invalid date - not a date before 7/9/2020'))

		if data <= data2:
			raise ValidationError(_('Invalid date - end date must be greater than start date'))

		# Remember to always return the cleaned data.
		return data

	def clean_start_urgency(self):
		data = self.cleaned_data['start_Urgency']
		
		if data < 0 or data > 5:
			raise ValidationError(_('Invalid Starting Urgency must be between 0 and 5'))

		# Remember to always return the cleaned data.
		return data


	def clean_end_urgency(self):
		data = self.cleaned_data['end_Urgency']
		data2 = self.cleaned_data['start_Urgency']
		
		if data < 0 or data > 5:
			raise ValidationError(_('Invalid Ending Urgency must be between 0 and 5'))
		if data <= date2:
			raise ValidationError(_('Invalid Ending Urgency - must great start urgency'))

		# Remember to always return the cleaned data.
		return data