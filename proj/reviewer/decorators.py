from tokenize import group
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if  request.user.is_authenticated:
            messages.add_message(request, messages.WARNING, 'User is Required to Logout first to perform the task.')
            return redirect('homepage')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()
            for item in group:
                if item.name in allowed_roles:
                    return view_func(request, *args, **kwargs)            
            messages.add_message(request, messages.WARNING, 'Premission not given to User!')
            return redirect('homepage')
        return wrapper_func
    return decorator
