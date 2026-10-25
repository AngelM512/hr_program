from typing import Any
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import RequestContext
from .models import Company, Profile, Company_Membership
from .forms import UserRegisterForm, UserUpdateForm, UpdateProfileForm
# Create your views here.

def register(request):
    #when a form is submitted, is recevied as a Post request
    if request.method == 'POST': # was the request a post request?
        # then create a new form
        form = UserRegisterForm(request.POST)

        if form.is_valid(): # is the form provided valid ? if true, then...

            new_user = form.save()  #save/create user in the database


            username = form.cleaned_data.get('username')
            id_username = form.cleaned_data.get('id_username')
            messages.success(request, f'Account created for {username}!')
            
            pf_created = Profile.objects.filter(user__username = username) #

            #create company + save the company object + instantiate user to company
            company_name = form.cleaned_data.get('company_name')
            company_addy = form.cleaned_data.get('company_address')
            company_inst = Company.objects.create(name = company_name, 
                                                address = company_addy, 
                                                profile = pf_created[0])
            company_inst.save()


            #company and user has been created now we have to assigned a membership

            membership = Company_Membership.objects.create(user = new_user,
                                                           company = company_inst,
                                                           role = Company_Membership.Assing_Role.ADMIN,
                                                
            )

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
            return redirect('company') #take user to the company's page

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

@login_required
def company_view(request):
  
    # GET company query of request.user of the user currently logged in
    query_set = Company_Membership.objects.filter(user=request.user) #user with membership

    company_id = request.GET.get('company_id')

    print("\ndegbug: company_id", company_id)
    #ON AND OFF BUTTOMS SET TO FALSE BY DEFAULT
    can_manage_employees = False
    can_user_add_or_del_employees = False

    if company_id:

        membership = query_set.filter(company_id=company_id).first()

        if membership is None:
            return HttpResponseForbidden('access denied')

        if membership.role == Company_Membership.Assing_Role.ADMIN:
            can_manage_employees = True
            can_user_add_or_del_employees = True

        elif membership.role == Company_Membership.Assing_Role.MANAGEMENT:
            can_user_add_or_del_employees = True


    
    context = {
            'company_qs' : query_set,
            'can_manage_employees' : can_manage_employees,
            'can_user_add_or_del_employees' : can_user_add_or_del_employees,
        }
    print("\ndegbug: company_id", company_id)

    
    return render(request, 'userMgt/company.html', context=context)

def get_company_employees(request):
    return render(request, 'userMgt/manage_employees.html', {})