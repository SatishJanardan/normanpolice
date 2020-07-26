from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Filelist(models.Model):
	fileName = models.CharField(max_length=250)

class Cat(models.Model):

	class Severitys(models.TextChoices):
		LOW = 'L'
		MEDIUM = 'M'
		HIGH = 'H'

	catName = models.CharField(max_length=50)
	catId = models.AutoField(primary_key=True)
	catSeverity = models.CharField(max_length=1,choices=Severitys.choices,default=Severitys.LOW)
	catUrgency = models.IntegerField(default=0)

class Crime(models.Model):

	class CaseOptions(models.TextChoices):  # Has this incident results in case being filed.
		NO = 'N'
		YES = 'Y'

	crimeDate = models.DateTimeField(default=timezone.now)
	crimeNumber = models.CharField(max_length=14)
	crimeLocation = models.CharField(max_length=50)
	crimeCatId = models.ForeignKey(Cat, on_delete=models.CASCADE)
	crimeORI = models.CharField(max_length=14)
	crimeLat = models.FloatField(default=35.221770)
	crimeLong = models.FloatField(default=-97.444960)
	crimeCase = models.CharField(max_length=1,choices=CaseOptions.choices,default=CaseOptions.NO)
	crimeArrest = models.CharField(max_length=1,choices=CaseOptions.choices,default=CaseOptions.NO)


	def __str__(self):
		return self.crimeNumber

	def get_absolute_url(self):
		return reverse('crime-detail', kwargs={'pk': self.pk})

class OffenseCat(models.Model):
	offenseCat = models.CharField(max_length=50)
	offenseCatId = models.AutoField(primary_key=True)

class Officer(models.Model):
	officerBadge = models.CharField(max_length=5)
	officerName = models.CharField(max_length=50,default="")
	officerId = models.AutoField(primary_key=True)

class Arrest(models.Model):
	arrestDate = models.DateTimeField(default=timezone.now)
	arrestNumber = models.CharField(max_length=14)
	arrestLocation = models.CharField(max_length=50)
	arrestOffenseId = models.ForeignKey(OffenseCat, on_delete=models.CASCADE)
	arrestArrestee = models.CharField(max_length=50)
	arrestBirthDate = models.DateTimeField(default=timezone.now)
	arrestArresteeAddr = models.TextField()
	arrestArresteeCity = models.CharField(max_length=20)
	arrestArresteeState = models.CharField(max_length=2)
	arrestArresteeZip = models.CharField(max_length=9)
	arrestArresteeStatus = models.CharField(max_length=14)
	arrestOfficerId = models.ForeignKey(Officer, on_delete=models.CASCADE)
	arrestLat = models.FloatField(default=35.221770)
	arrestLong = models.FloatField(default=-97.444960)
	arrestFileDate = models.DateField(default='2020-06-01')

	def __str__(self):
		return self.arrestNumber

	def get_absolute_url(self):
		return reverse('arrest-detail', kwargs={'pk': self.pk})

class Case(models.Model):
	caseDate = models.DateTimeField(default=timezone.now)
	caseNumber = models.CharField(max_length=14)
	caseLocation = models.CharField(max_length=50)
	caseOffenseId = models.ForeignKey(OffenseCat, on_delete=models.CASCADE)
	caseOfficerId = models.ForeignKey(Officer, on_delete=models.CASCADE)
	caseLat = models.FloatField(default=35.221770)
	caseLong = models.FloatField(default=-97.444960)
	caseFileDate = models.DateField(default='2020-06-01')

	def __str__(self):
		return self.caseNumber

	def get_absolute_url(self):
		return reverse('case-detail', kwargs={'pk': self.pk})

class Weather(models.Model):

	wMonth = models.IntegerField()
	wDay = models.IntegerField()
	wTempMax = models.IntegerField()
	wTempAvg = models.FloatField()
	wTempMin = models.IntegerField()
	wDewMax = models.IntegerField()
	wDewAvg = models.FloatField()
	wDewMin = models.IntegerField()
	wHumidityMax = models.IntegerField()
	wHumidityAvg = models.FloatField()
	wHumidityMin = models.IntegerField()
	wWindMax = models.IntegerField()
	wWindAvg = models.FloatField()
	wWindMin = models.IntegerField()
	wPressureMax = models.FloatField()
	wPressureAvg = models.FloatField()
	wPressureMin = models.FloatField()
	wPrecipitation = models.FloatField()

class Graphdata(models.Model):
	bucket_Size = models.IntegerField(default=5)
	start_Date = models.DateTimeField(default='2020-06-01 00:00:00')
	end_Date = models.DateTimeField(default='2020-07-09 12:00:00')
	start_Urgency = models.IntegerField(default=0)
	end_Urgency = models.IntegerField(default=5)

