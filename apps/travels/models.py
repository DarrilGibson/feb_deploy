from __future__ import unicode_literals
from django.db import models
from .. loginreg.models import User
import re, datetime

REGEX_DATE = r'/(0[1-9]|1[012])[- \/.](0[1-9]|[12][0-9]|3[01])[- \/.](19|20)\d\d/';

class TravelManager(models.Manager):
    def add_trip (self, data, user_id):
        errors=[]
        print data
        destination = data['destination']
        plan = data['plan']
        begintrip = data['travelstartdate']
        endtrip = data['travelenddate']
        today = datetime.datetime.now
        print "dates"
        print today
        strtoday = str(today)
        print strtoday
        # today2 = datetime.date.now()
        # print today2

        # dtnow = str(datetime.datetime.now())
        # print dtnow
        # dtonlynow = datetime.datetime.strptime(today,"%Y-%m-%d")
        # print dtonlynow

        # Validation for item
        print destination
        if len(destination) == 0:
            errors.append('Please enter a destination.')
        elif len(destination) < 4:
            errors.append('Please be more descriptive with the desination.')

        if len(plan) == 0:
            errors.append('Please enter a plan.')
        elif len(plan) < 4:
            errors.append('Please add more letters to descripe this trip.')

        # start = travelstartdate
        # print "travelstartdate"
        # print start
        # print startstamp

        # dtstart = datetime.datetime.strptime(travelstartdate,"%m/%d/%Y")
        if len(endtrip) == 0:
            errors.append('Please enter a travel start date.')
        # elif not re.match(REGEX_DATE,travelstartdate):
        #     errors.append('Please enter dates in the format of mm/dd/yyyy (such as 02/29/2016).')
        # elif travelstartdate < Now():
        #     errors.append('Flux capacitors are not available yet. Please enter a date in the future.')
        #
        if len(begintrip) == 0:
            errors.append('Please enter a travel end date.')
        # elif not re.match(REGEX_DATE,travelstartdate):
        #     errors.append('Please enter dates in the format of mm/dd/yyyy (such as 02/29/2016).')
        # elif travelenddate < travelstartdate:
        #     errors.append('Please enter an end date that is after the start date.')

        if errors:
            print errors
            return(False,errors)
        else: # no errors - write to database
            traveler = User.objects.get(id=user_id)
            print "writing item"
            # print travelenddate
            # print item
            action = self.create(destination=destination,plan=plan, traveler=traveler, begintrip=begintrip, endtrip=endtrip)
            # , travel_start_date=travelstartdate)
            # , travel_end_date=travelenddate)
            action.save()
            return(True, errors)

    def add_other_trip (self, item_id, user_id):
        print "in addother trip"
        # Two steps. 1) Retrieve plan, 2) add
        trip_obj = self.get(id=item_id)
        plan = trip_obj.plan
        destination = trip_obj.destination
        endtrip = trip_obj.endtrip
        begintrip = trip_obj.begintrip
        traveler = User.objects.get(id=user_id)
        print traveler
        action = self.create(destination=destination,plan=plan,traveler=traveler,begintrip=begintrip, endtrip=endtrip)
        action.save()
        return(True)

class Travel(models.Model):
    destination = models.CharField(max_length=255)
    begintrip = models.CharField(max_length=20)
    endtrip = models.CharField(max_length=20)
    # travel_start_date = models.DateTimeField()
    # travel_end_date = models.DateTimeField()
    plan = models.CharField(max_length=255)
    # description = models.CharField(max_length=255)
    # is description a reserved word?
    traveler = models.ForeignKey(User, related_name="traveling_user")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # Connect UserManager to User class to add methods
    objects = TravelManager()
