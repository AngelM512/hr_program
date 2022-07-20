from typing import Any
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import RequestContext
from .models import Company, Profile
from .forms import UserRegisterForm, UserUpdateForm, UpdateProfileForm
from django.contrib.auth.models import User
# Create your views here.

def register(request):
    #when a form is submitted, is recevied as a Post request
    if request.method == 'POST': # was the request a post request?
        # then create a new form
        form = UserRegisterForm(request.POST)

        if form.is_valid(): # is the form provided valid ? if true, then...
            form.save() #save/create user in the database


            username = form.cleaned_data.get('username')
            id_username =form.cleaned_data.get('id_username')
            messages.success(request, f'Account created for {username}!')
            
            
            #get user
            pf_qs = Profile.objects.all()
            pf_created = Profile.objects.filter(user__username = username)

            #create company + save the company object + instantiate user to company
            company_name = form.cleaned_data.get('company_name')
            company_addy = form.cleaned_data.get('company_address')
            company_inst = Company.objects.create(name = company_name, 
                                                address = company_addy, 
                                                profile = pf_created[0])
            company_inst.save()
            
                                    # if user was created successfully then,
            return redirect('login-home')    # take client to the loginpage


    else:
        form = UserRegisterForm()

    return render(request, 'userMgt/register.html', { 'form':form } )


@login_required(login_url='/login/') # must loging in order to have access to your profile
def profile(request):
    if request.method == 'POST':
        Uform = UserUpdateForm(request.POST, instance=request.user)
        Pform = UpdateProfileForm( request.POST,
                                   request.FILES,
                                   instance=request.user.profile
                                   )
        #if the forms are valid; save and take user to the homepage
        if Uform.is_valid() and Pform.is_valid():
            #save
            Uform.save()
            Pform.save()
            #provide user with some feedback
            messages.success(request, 'Profile has been updated!')
            return redirect('blog-home') #take user to the homepage

    else:
        Uform = UserUpdateForm(instance=request.user)
        Pform = UpdateProfileForm(instance=request.user.profile)

    context = {
        'Uform': Uform,
        'Pform': Pform,
    }
    return render(request, 'userMgt/profile.html', context)


#-------------------------------------------------------------------------------------#
# company view will be able to create and manage company, see tools, employees etc.. 
def company_view(request):
    context = {}
    return render(request, 'userMgt/company.html', context=context)

def get_company_employees(request):
    return render(request, 'userMgt/manage_employees.html', {})