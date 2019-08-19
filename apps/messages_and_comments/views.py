from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import datetime

def index(request):
    if 'curUser' not in request.session:
        return redirect('/')
    all_messages = Messages.objects.all()
    for message in all_messages:
        print(message)
        created = message.created_at
        date_string = created.strftime('%B %d{suffix} %Y')
        day = created.day
        if 3 < day < 21 or 23 < day < 31:
            the_suffix = 'th'
        else:
            the_suffix = {1: 'st', 2: 'nd', 3: 'rd'}[day % 10]
        message.created_at = date_string.format(suffix=the_suffix)
    reversed_messages = all_messages[::-1]
    context = {'user' : Users.objects.get(email = request.session['curUser']), 
                'wall_messages' : reversed_messages
    }
    return render(request, 'messages_and_comments/index.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def create_message(request):
    errors = Messages.objects.message_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wall')
    Messages.objects.create(content = request.POST['content'], message_owner = Users.objects.get(email = request.session['curUser']))
    return redirect('/wall')

def create_comment(request):
    errors = Comments.objects.comment_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wall')
    Comments.objects.create(content = request.POST['content'], related_message = Messages.objects.get(id = request.POST['message_id']),
                             comment_owner = Users.objects.get(email = request.session['curUser']))
    return redirect('/wall')

def delete_comment(request):
    comment = Comments.objects.get(id = request.POST['comment_id'])
    comment.delete()
    return redirect('/wall')

def delete_message(request):
    message = Messages.objects.get(id = request.POST['message_id'])
    message.delete()
    return redirect('/wall')
