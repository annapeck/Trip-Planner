from __future__ import unicode_literals
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import bcrypt
from datetime import datetime


class UserManager(models.Manager):
	def regValidator(self, postData):
		errors = {}
		if User.objects.filter(email = postData['email']):
		 	errors['email_exists'] = "An account associated with that email address already exists."
		if len(postData['first_name']) < 3 or not postData['first_name'].isalpha():
			errors['first_name'] = "First name must be at least 3 characters long, and use only alphabetical characters."
		if len(postData['last_name']) < 3 or not postData['last_name'].isalpha():
			errors['last_name'] = "Last name must be at least 3 characters long, and use only alphabetical characters."
		if EMAIL_REGEX.match(postData['email']) == None:
			errors['email_format'] = "Email must be in valid email format."
		if len(postData['password']) < 8:
			errors['password_length'] = "Password must be at least 8 characters long."
		if postData['password'] != postData['passwordconfirm']:
			errors['passwordconfirm'] = "Password confirmation must match password."
		print(errors)
		return errors
	def loginValidator(self, postData):
		user = User.objects.filter(email = postData['login_email'])
		errors = {}
		if not user:
			errors['email'] = "Please enter a valid email address."
		if user and not bcrypt.checkpw(postData['login_password'].encode('utf8'), user[0].password.encode('utf8')):
			errors['password'] = "Invalid password."
		return errors

class TripManager(models.Manager):
	def TripValidation(request, postData):
		errors = {}
		if len(postData['destination']) < 1:
			errors["destination"] = "Must input a destination"
		if len(postData['description']) < 1:
			errors["lastname"] = "Must input a description"
		if len(postData['travelstart']) < 1:
			errors['travelstartlen'] = "Start Date can't be blank"
		elif postData['travelstart'] < str(datetime.now()):
			errors['travelstartpast'] = "Start Date can't be in the past"
		if len(postData['travelend']) < 1:
			errors['travelendlen'] = "End Date can't be blank"
		elif postData['travelend'] < str(datetime.now()):
			errors['travelendpast'] = "End date can't be in the past"
		if postData['travelstart'] > postData['travelend']:
			errors['wrongrange'] = "Your start date is after the end date"
		return errors



class User(models.Model):
	first_name = models.CharField(max_length = 255)
	last_name = models.CharField(max_length = 255)
	email = models.CharField(max_length = 255)
	password = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()
	def __repr__(self):
		return "<User object: {} {}>".format(self.first_name, self.last_name, self.email)


class Trip(models.Model):
	destination = models.TextField(max_length=100)
	description = models.TextField(max_length=150)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	creator = models.IntegerField(max_length = 255)
	user = models.ManyToManyField(User, related_name = "trips")
	objects = TripManager()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)








