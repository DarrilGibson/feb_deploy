from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from . models import User

def index(request):
	return render(request, 'loginreg/index.html')

def register(request):
    if request.method == "POST":
		# session data: firstname, lastname, email, id, "True if logged in"
		request.session['firstname'] = request.POST['firstname']
		request.session['email'] = request.POST['email']
		success, user_manager_response = User.objects.register(request.POST)
		print success
		print user_manager_response
		if success: # user registered
			print "success user registered"
			request.session['user_id'] = user_manager_response
			print "user id"
			print request.session['user_id']
			request.session['login'] = "True"
			# msg = "You have successfully registered and are currently logged in."
			# messages.success(request, msg)
			return redirect('travels:index')
		else:
			request.session['lastname'] = request.POST['lastname']
			request.session['email'] = request.POST['email']
			for error in user_manager_response:
			    messages.error(request, error)
			return redirect('/')
    else: #request.method != POST
        return redirect('/')

def success(request):
    return render(request, "loginreg/success.html")

def show(request): #show existing users
	if 'login' not in request.session: # not logged in
	    return redirect('/') # send to login page
	else:
		request.session
		users = User.objects.all()
		print users
		context = {
			"users": users
		}
		return render(request, "loginreg/show.html", context)

def edit(request, id): #show single user for editing
	# id is user_id
	if 'login' not in request.session: # not logged in
	    return redirect('/') # send to login page
	else:
		request.session['edit_id'] = id
		users = User.objects.filter(id=id)
		print users
		context = {
			"users": users
		}
		return render(request, "loginreg/edituser.html", context)

def edituser(request): #update single user
    if request.method == "POST":
		print "in views:edituser"
		# session data: firstname, lastname, email, id, "True if logged in"
		success, user_manager_response = User.objects.updateuser(request.POST)
		if success: # user modified
			print "success user updated"
			users = User.objects.all()
			context = {
				"users": users
			}
			return render(request, "loginreg/show.html", context)
		else:
			request.session['editfirstname'] = request.POST['editfirstname']
			request.session['editlastname'] = request.POST['editlastname']
			request.session['editemail'] = request.POST['editemail']
			for error in user_manager_response:
			    messages.error(request, error)
			id = request.session['edit_id']
			users = User.objects.filter(id=id)
			print users
			context = {
				"users": users
			}
			return render(request, "loginreg/edituser.html", context)
    else: #request.method != POST
        return redirect('/')

def destroy(request, id):
	print "in destroy"
	action = User.objects.deleteuser(id)
	msg = "User deleted."
	messages.success(request, msg)
	print "user deleted"
	# return redirect('show')
	users = User.objects.all()
	context = {
		"users": users
	}
	return render(request, "loginreg/show.html", context)

def logout(request):
	request.session.clear()
	return redirect('/')

def login(request):
    if request.method == "POST":
		print "in login"
		# email named differently to prevent automatic populating during register
        # session data: firstname, lastname, email, id, "True if logged in"
		request.session['loginemail'] = request.POST['loginemail']
		success, user_manager_response, user_id = User.objects.login(request.POST)
		# success, user_manager_response = User.objects.login(request.POST)
		if success == True: # login successful
			print "login successful"
			# store user data in session
			request.session['firstname'] = user_manager_response
			request.session['user_id'] = user_id
			request.session['login'] = "True"
			print request.session['firstname']
			print request.session['user_id']
			return redirect('travels:index')
		else: #errors
			request.session['loginmsg'] = "Incorrect email address or password."
			return render(request, 'loginreg/index.html')
    else: #request.method != POST
        return redirect('/')
