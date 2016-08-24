from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
from datetime import datetime, timedelta, date, time
from time import strftime
from ..loginapp.models import Userlog

class UserManager(models.Manager):
	def task(self,task):
		if not len(task) > 1:
			return(False,"Description can't be empty")
		else:
			return(True,task)
	def date_check(self,appdate):
		appt_date = appdate
		today = strftime('%Y-%m-%d')
		if appt_date == "" or appt_date < today:
			return(False, "Please enter date!")
		return(True, appdate)

	def time_check(self,time):
		time_log = time
		if time_log == "":
			return(False, "Please enter a time!")
		else:
			return(True, time)

	def Update(self, id, data):
		errors = []
		Appointments = Appointment.objects.get(id=id)
		Appointments.task = data['task']
		Appointments.date = data['appdate']
		Appointments.time = data['time']
		Appointments.status = data['status']
		today = strftime('%Y-%m-%d')
		if data['appdate'] == "" or data['appdate'] < today:
			errors.append("Date can't be empty")
		if data['time'] == "":
			errors.append("Please enter a time")
		if len(data['task']) < 1:
			errors.append("Task can't be empty")
		if errors:
			return(False,errors)
		if not errors:
			Appointments.save()
			return (True,Appointment)

class Appointment(models.Model):
	user = models.ForeignKey('loginapp.Userlog', related_name='users')
	task = models.CharField(max_length=30)
	date = models.DateField()
	time = models.TimeField()
	status = models.CharField(max_length=30)
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)
	UserManager = UserManager()
	objects = models.Manager()
