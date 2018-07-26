from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt
from datetime import datetime

def index(request):
	if 'logged_in' not in request.session:
		request.session['logged_in'] = False
	if 'email' in request.session:
		del request.session['email']
		request.session['logged_in'] = False
	return render(request, 'login_app/index.html')

def register(request):
	msgs = User.objects.regValidator(request.POST)
	if len(msgs):
		for k,v in msgs.items():
			print( k,v)
			messages.error(request, v, extra_tags=k)
			
	else:
		hashedpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
		u = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email=request.POST['email'], password=hashedpw)
		request.session['id'] = u.id
		print(request.session['logged_in'])
		return redirect('/display')

	return redirect('/')

def login(request):
	errors = User.objects.loginValidator(request.POST)
	if request.method == 'POST':
		if len(errors):
			for key, value in errors.items():
				messages.error(request, value)
			return redirect('/')
		else:
			user = User.objects.get(email=request.POST['login_email'])
			request.session['id'] = user.id
			return redirect('/display')

def delete(request):
	del(request.session['id'])
	return redirect('/')

def edit(request, id):
	context ={
		'user': User.objects.get(id=request.session['id'])

	}

	return render(request, 'login_app/myaccount.html', context)

def editpage(request, id):
	u = User.objects.get(id=id)
	u.first_name = request.POST['first_name']
	u.last_name = request.POST['last_name']
	u.email = request.POST['email']
	u.save()

	return redirect('/success')

def display(request):
	context ={
		'user': User.objects.get(id=request.session['id']),
		'usertrips': User.objects.get(id=request.session['id']).trips.all(),
		'othertrips': Trip.objects.exclude(user=request.session['id']),
	}
	return render(request, 'login_app/success.html', context)

def addtrip(request):
	return render(request, 'login_app/addtrip.html')

def addtrip_db(request):
	errors = Trip.objects.TripValidation(request.POST)
	if len(errors):
		for key, value in errors.items():
			messages.error(request,value)
		print(messages.error)
		return render(request, 'login_app/addtrip.html')
	else:
		user = User.objects.get(id=request.session['id'])
		user.save()
		new_trip = Trip.objects.create(destination = request.POST['destination'], description = request.POST['description'], start_date = request.POST['travelstart'], end_date = request.POST['travelend'], creator = request.session['id'])
		new_trip.save()
		new_trip.user.add(user)
		return redirect('/display')
	return redirect('/display')

def view(request, id):
	trip = Trip.objects.get(id=id)
	context = {
		'destination': trip.destination,
		'description': trip.description,
		'start_date': trip.start_date,
		'end_date': trip.end_date,
		'created_by': User.objects.get(id=trip.creator).first_name,
		'all_travelers': trip.user.exclude(id=trip.creator)
	}
	return render(request, 'login_app/tripview.html', context)

def cancel(request, id):
	trip = Trip.objects.get(id=id)
	trip.save()
	user= User.objects.get(id=request.session['id'])
	trip.user.remove(user)
	return redirect('/display')
def delete(request, id):
	trip = Trip.objects.get(id=id)
	trip.delete()
	return redirect('/display')

def join(request, id):
	trip = Trip.objects.get(id=id)
	trip.save()
	new_user = User.objects.get(id=request.session['id'])
	new_user.save()
	trip.user.add(new_user)
	return redirect('/display')





































