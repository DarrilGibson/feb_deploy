from __future__ import unicode_literals
from django.db import models
import bcrypt, re

# Email name regex patterns

REGEX_EMAIL=r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$'
#instructions say letters only Modified
# - allows a dash, \s allows a space,  \' allows apostrophe
# Realistically, check only for minimum and maximum characters
REGEX_NAME= r'^([a-zA-Z]*)([-\s\'][a-zA-Z]*)*$'
# regex_name= r'^[a-zA-Z]*$'

class UserManager(models.Manager):
    def register (self, data):
        print "in UserManager register"
        errors = []
        first_name = data['firstname']
        last_name = data['lastname']
        email = data['email'] #register email
        password = data['password']
        confirm_pw = data['confirm_pw']

        if len(first_name) < 3:
            errors.append("Please enter your first name.")
        elif not re.match(REGEX_NAME,first_name):
            errors.append("Please enter only letters in your first name.")

        if len(last_name) < 3:
            errors.append("Please enter your last name.")
        elif not re.match(REGEX_NAME,last_name):
            errors.append("Please enter only letters in your last name.")

        if len(email) == 0:
            errors.append("Please enter your email address.")
        elif not re.match(REGEX_EMAIL,email):
            errors.append("Please enter a valid email address.")
        else: # duplicate_email_check
            if User.objects.filter(email=email).exists():
                errors.append("That email address already exists in the database. Please enter a different email address.")

        if len(password) < 8:
            errors.append("Your password must be at least 8 characters long.")
        elif password != confirm_pw:
            errors.append("Your passwords don't match.")
        else:
            pw = password.encode()
            hashpassword = bcrypt.hashpw(pw,bcrypt.gensalt())
        if errors:
            print errors
            return(False, errors)
        else: #No errors. Write user to database
            action =self.create(first_name=first_name,last_name=last_name,email=email,password=hashpassword)
            action.save()
            errors = []
            user = User.objects.get(email=email)
            user_id=user.id
            print user
            print user_id
            return (True, user_id)

    def login (self, data):
        # check for email first
        email = data['loginemail']
        password = data['password']
        if User.objects.filter(email=email).exists(): # email is in database
            user = User.objects.get(email=email) # Get user object
            first_name = user.first_name
            user_id=user.id
            userpw = user.password.encode() # stored password for user
            provided_pw = password.encode()
            if bcrypt.hashpw(provided_pw, userpw) == userpw:
                print "passwords match"
                user = User.objects.get(email=email) # Get user object
                return (True, first_name, user_id)
            else:
                msg="passwords don't match"
                return (False, email, password)
        else: # email doesn't exist
            return (False, email, password)

    def deleteuser (self, id):
        print "in delete user"
        action = self.get(id=id)
        print "action"
        print action
        action.delete()
        return (True)

    def updateuser (self,data):
        print "in UserManager updateuser"
        errors = []
        first_name = data['editfirstname']
        last_name = data['editlastname']
        email = data['editemail']

        if len(first_name) < 3:
            errors.append("Please enter the first name for this user.")
        elif not re.match(REGEX_NAME,first_name):
            errors.append("Please enter only letters in the first name.")

        if len(last_name) < 3:
            errors.append("Please enter the last name for this user.")
        elif not re.match(REGEX_NAME,last_name):
            errors.append("Please enter only letters in the last name.")

        if errors:
            print errors
            return(False, errors)
        else: #No errors. Write user to database
            user = User.objects.get(email=email)
            user.first_name = first_name
            user.last_name = last_name
            # action = user.update(first_name=first_name,last_name=last_name)
            # action = self.update(first_name=first_name,last_name=last_name)
            user.save()
            errors = []
            return (True, errors)

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # Connect UserManager to User class to add methods
    objects = UserManager()
    # Hidden from Travel FK related_name= "traveling_user"
