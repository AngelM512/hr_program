from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm
# Create your views here.



def register(request):
    #when a form is submitted, is recevied as a Post request
    if request.method == 'POST': # was the post request a post request?
        # then create a new form
        form = UserRegisterForm(request.POST)

        if form.is_valid(): # is the form provided valid ? if true, then...

            form.save() #save/create user in the database

            username = form.cleaned_data.get('username')

            messages.success(request, f'Account created for {username}!')
                                        # if user was created successfully
            return redirect('Login')# take client to the homepage


    else:

        form = UserRegisterForm()

    return render(request, 'userMgt/register.html', { 'form':form } )



@login_required(login_url='/login/') # must loging in order to have access to your profile
def profile(request):

    return render(request, 'userMgt/profile.html')
