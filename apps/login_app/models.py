from __future__ import unicode_literals
from django.db import models
import datetime

class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        if 'first_name' in postData:
            if len(postData['first_name']) < 2:
                errors['first_name'] = "First name must be at least two characters long"
            if len(postData['last_name']) < 2:
                errors['last_name'] = "Last name must be at least two characters long"
            if len(postData['regPassword']) < 8:
                errors['pw_length'] = "Password must be at least eight characters long"
            if postData['regPassword'] != postData['confPassword']:
                errors['pw_match'] = "Passwords do not match!"
            if postData['date'] > str(datetime.date.today()):
                errors['date'] = "You're not a time traveler!"
            today = datetime.date.today() 
            birthDate = postData['date'].split('-')
            age = today.year - int(birthDate[0]) - ((today.month, today.day) < (int(birthDate[1]), int(birthDate[2]))) 
            if age < 13:
                errors['age'] = "The user must be 13 years or older!"
        return errors

class Users(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255) 
    birthdate = models.DateField()
    pw_hash = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()