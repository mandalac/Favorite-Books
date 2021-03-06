from django.db import models
import re

class UserManager(models.Manager):
    def registrationValidator(self, postData):
        errors = {}
        try:
            User.objects.get(email = postData['email'])
            errors['email'] = 'Email adress already exists'
        except:
            pass
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid email adress'
        if len(postData['first_name'])<2:
            errors['first_name'] = 'First name sould be minimum 2 characters'
        if len(postData['last_name'])<2:
            errors['last_name'] = 'Last name sould be minimum 2 characters'
        if len(postData['password'])<8:
            errors['password'] = 'Password sould be minimum 8 characters'
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords didn't match"
        return errors

class BookManager(models.Manager):
    def bookValidator(self, postData):
        errors={}
        if len(postData['title'])<2:
            errors['title'] = 'Title should have at least 1 character'
        if len(postData['description'])<2:
            errors['description'] = 'Description should have at least 1 character'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 320)
    password = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length = 45)
    description = models.TextField()
    uploader = models.ForeignKey(User, related_name='book_uploader', on_delete= models.CASCADE)
    favorites = models.ManyToManyField(User, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BookManager()