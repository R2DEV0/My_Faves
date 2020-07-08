from django.db import models
import re, bcrypt

class ShowManager(models.Manager):

    # validations for new user # 
    def new_validator(self, postData):
        user = User.objects.filter(email=postData['email'])
        errors= {}
        if (len(postData['name']) < 2):
            errors['name'] = 'Your name should be at least 2 characters long.'
        if (len(postData['home']) < 2):
            errors['home'] = 'Please enter a valid city.'
        if (len(postData['password']) < 5):
            errors['password'] = 'Password must be at least 5 characters long.'
        if postData['confirmed_pass'] != postData['password']:
            errors['password'] = 'Password must match the confirmation.'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):       
            errors['email'] = "Invalid email address."
        if user:
            errors['email'] = "Email already registered"
        else:
            pass
        return errors

    # validations for returning user # 
    def return_validator(self, postData):
        errors = {}
        user = User.objects.filter(name=postData['name'])
        if (len(postData['name']) < 1):
            errors['name'] = "Name was not entered."
        if (len(postData['password']) < 1):
            errors['password'] = "Password was not entered."
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                return errors
            else:
                errors['no_pass'] = 'Incorrect password'
        errors['no_name'] = 'User name is not registered'
        return errors

    # validations for new city #
    def city_validator(self, postData):
        errors = {}
        if (len(postData['name']) <3):
            errors['name'] = 'City must be at least 3 characters'
        return errors

    # validations for new liked activity #
    def like_validator(self, postData):
        errors = {}
        if (len(postData['name']) <3):
            errors['name'] = 'Activity must be at least 3 characters'
        return errors


class User(models.Model):
    name= models.CharField(max_length=255)
    home= models.CharField(max_length=100)
    email= models.CharField(max_length= 255)
    password= models.CharField(max_length= 255)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects = ShowManager()

class City(models.Model):
    name= models.CharField(max_length=100)
    user= models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects = ShowManager()

class Likes(models.Model):
    name= models.CharField(max_length=255)
    user= models.ForeignKey(User, related_name='l_users', on_delete=models.CASCADE)
    city= models.ForeignKey(City, related_name='l_cities', on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects = ShowManager()