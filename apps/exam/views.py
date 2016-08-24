from django.shortcuts import render,redirect, HttpResponse
from ..loginapp.models import Userlog
from .models import Appointment
from django.contrib import messages
from datetime import datetime
from django.core.urlresolvers import reverse
import bcrypt

def user(request):
	errors = False
	validation1 = Appointment.UserManager.task(request.POST['task'])
	validation2 = Appointment.UserManager.date_check(request.POST['appdate'])
	validation3 = Appointment.UserManager.time_check(request.POST['time'])

	if validation1[0] == False:
		messages.add_message(request, messages.INFO, "Invalid Task", extra_tags="regtag")
		errors = True
	if validation2[0] == False:
		messages.add_message(request, messages.INFO, "Invalid Date", extra_tags="regtag")
		errors = True
	if validation3[0] == False:
		messages.add_message(request, messages.INFO, "Invalid Time", extra_tags="regtag")
		errors = True
	if errors == True:
		return redirect('/appointments')
	elif (validation1[0] == True & validation2[0] == True & validation3[0] == True):
		users = Userlog.objects.get(name = request.session['user'])
		Appointment.objects.create(user = users ,task=validation1[1], date=validation2[1], time=validation3[1], status='pending')
		return redirect('/appointments')

def edit(request, task_id):
	context={
		'updates' : Appointment.objects.filter(id=task_id)
	}
	return render(request, 'exam/show.html', context)

def update(request, task_id):
	app_update = Appointment.UserManager.Update(task_id, request.POST)
	if app_update[0] == False:
		for error in app_update[1]:
			messages.add_message(request, messages.INFO, error)
		return redirect(reverse('gohere',kwargs={'task_id':task_id}))
	else:
		return redirect('/appointments')

def destroy(request, task_id):
	Appointment.objects.get(id=task_id).delete()
	return redirect('/appointments')
