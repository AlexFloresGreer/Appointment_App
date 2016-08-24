from django.shortcuts import render,redirect, HttpResponse
from .models import Userlog
from django.contrib import messages
from ..exam.models import Appointment
from datetime import datetime
from django.db.models import Q
import bcrypt

def index(request):
	return render(request,'loginapp/index.html')
def success(request):
	now = datetime.now()
	context={
	'today': datetime.now().date(),
	'today_appt': Appointment.objects.filter(Q(date__lte=now, date__gte=now) & Q(user__name=request.session['user'])).order_by('time'),
	'future_appt': Appointment.objects.filter(Q(date__gte=now) & Q(user__name=request.session['user'])).exclude(date__lte=now, date__gte=now).order_by('date')
	}
	return render(request,'exam/success.html',context)
def user(request):
	errors = False
	validation1 = Userlog.UserManager.first_name(request.POST['name'])
	validation2 = Userlog.UserManager.user_name(request.POST['username'])
	validation3 = Userlog.UserManager.password(request.POST['password'])
	validation3_char = Userlog.UserManager.password_charcheck(request.POST['password'])
	validation4 = Userlog.UserManager.confirm_password(request.POST['password'],request.POST['confirm_password'])
	validation5 = Userlog.UserManager.birthday(request.POST['birthday'])
	if validation1[0] == False:
		messages.add_message(request, messages.INFO, "Invalid name", extra_tags="regtag")
		errors = True
	if validation2[0] == False:
		messages.add_message(request, messages.INFO, "Invalid username", extra_tags="regtag")
		errors = True
	if validation3[0] == False:
		messages.add_message(request, messages.INFO, "Invalid password", extra_tags="regtag")
		print validation4[1]
		errors = True
	if validation3_char[0] == False:
		messages.add_message(request, messages.INFO, "Invalid characters in password", extra_tags="regtag")
		errors = True
	if validation4[0] == False:
		messages.add_message(request, messages.INFO, "Password does not match!", extra_tags="regtag")
		errors = True
	if validation5[0] == False:
		print validation5[1]
		messages.add_message(request, messages.INFO, "Invalid birthdate", extra_tags="regtag")
		errors = True
	if Userlog.objects.filter(username = request.POST['username']):
	    messages.add_message(request, messages.INFO, "Username exists already!", extra_tags="regtag")
	    errors = True
	# Errors Route
	if errors == True:
		return redirect('/')
	elif (validation1[0] == True & validation2[0] == True  & validation3[0] == True ):
		Userlog.UserManager.create(name=validation1[1], username=validation2[1], password=validation3[1],birthday=validation5[1])
		request.session['user'] = validation1[1]
		print
		return redirect('/appointments')

def login(request):
	validation6 = Userlog.UserManager.log(request.POST['username'], request.POST['password'])
	if validation6[0] == False:
		messages.add_message(request, messages.INFO, validation6[1], extra_tags='logtag')
		print validation6[1]
		return redirect('/')
	else:
		request.session['user'] = validation6[1]
		return redirect('/appointments')

def logout(request):
	del request.session['user']
	return redirect('/')
