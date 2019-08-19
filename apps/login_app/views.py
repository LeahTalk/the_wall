from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
import re

def index(request):
    return render(request, 'login_app/index.html')

def user_homepage(request):
    if 'curUser' not in request.session:
        return redirect('/')
    context = {'user' : Users.objects.get(email = request.session['curUser'])}
    return render(request, 'login_app/user_homepage.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def login(request):
    errors = Users.objects.user_validator(request.POST)
    user = Users.objects.filter(email=request.POST['email'])
    print(user)
    if user: 
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.pw_hash.encode()):
            request.session['curUser'] = logged_user.email
            return redirect('/wall')
        else:
            errors['badPassword'] = "The password is incorrect."
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
    else:
        errors['noUser'] = "There is no user with this email address!"  
        for key, value in errors.items():
            messages.error(request, value)  
        return redirect("/")

def register(request):
    errors = Users.objects.user_validator(request.POST)
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if not EMAIL_REGEX.match(request.POST['email']):        
        errors['email'] = ("Invalid email address!")
    if Users.objects.filter(email=request.POST['email']).exists():
        errors['exists'] = "A user with this email already exists!"
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['regPassword']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())  # create the hash    
        Users.objects.create(first_name=request.POST['first_name'], last_name = request.POST['last_name'],
                    email = request.POST['email'], birthdate = request.POST['date'], pw_hash=pw_hash)
        request.session['curUser'] = request.POST['email']
        return redirect('/wall')
