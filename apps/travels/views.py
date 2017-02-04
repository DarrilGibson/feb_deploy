from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from datetime import datetime
from . models import Travel

def index(request):
    print "in travels:index"
    # return render(request, 'travels/index.html')
    # check for session
    # alltravels = Travel.objects.all().prefetch_related('traveler')
    # print alltravels.first_name

    if 'login' not in request.session: # not logged in
        print "not logged in"
        return redirect('/') # send to login page
    else: #logged in
        print request.session['firstname']
        user_id = request.session['user_id']
        context = {
            "alltravels": Travel.objects.all().prefetch_related('traveler'),
            "usertravels": Travel.objects.filter(traveler__id=user_id),
            # "usertravels": Travel.objects.all(),
            # "alltravels": Travel.objects.all()
            }
        return render(request, 'travels/index.html', context)

def create(request):
    if request.method == "POST":
        print request.session['user_id']
        user_id = request.session['user_id']
        success, travel_manager_response=Travel.objects.add_trip(request.POST, user_id)
        if success:
            #no errors
            print "success"
            context = {
            "alltravels": Travel.objects.all().prefetch_related('traveler'),
            "usertravels": Travel.objects.filter(traveler__id=user_id),
            }
            return render(request, 'travels/index.html', context)
        else:
            request.session['destination'] = request.POST['destination']
            request.session['plan'] = request.POST['plan']
            print request.session['plan']
            request.session['travelstartdate'] = request.POST['travelstartdate']
            request.session['travelenddate'] = request.POST['travelenddate']
            for error in travel_manager_response:
                messages.error(request, error)
                request.session.error = error
            cur_date = datetime.now().strftime ("%B %d, %Y")
            context = {
                "cur_date":cur_date
            }
            return render(request, 'travels/create.html', context)
    else: #request.method != POST
        return render(request, 'travels/create.html')

    return redirect('/')    #users/create

def show(request):
    if 'login' not in request.session: # not logged in
        return redirect('/') # send to login page
    else: #logged in
        cur_date = datetime.now().strftime ("%B %d, %Y")
        context = {
            "cur_date":cur_date
        }
        return render(request, 'travels/create.html', context)

def addother(request, id):
    print "in add other"
    #id = trip id
    print request
    user_id = request.session['user_id']
    print user_id
    print id
    success=Travel.objects.add_other_trip(id, user_id)
    if success: #no errors
        print "success"
        context = {
            "alltravels": Travel.objects.all().prefetch_related('traveler'),
            "usertravels": Travel.objects.filter(traveler__id=user_id),            }
        return render(request, 'travels/index.html', context)

def logout(request):
	request.session.clear()
	return redirect('/')
