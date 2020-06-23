from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, UpdateProfileForm
# Create your views here.



def register(request):
    #when a form is submitted, is recevied as a Post request
    if request.method == 'POST': # was the request a post request?
        # then create a new form
        form = UserRegisterForm(request.POST)

        if form.is_valid(): # is the form provided valid ? if true, then...

            form.save() #save/create user in the database

            username = form.cleaned_data.get('username')

            messages.success(request, f'Account created for {username}!')
                                    # if user was created successfully then,
            return redirect('Login')    # take client to the loginpage


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
        #if the forms are valid save and take user to the homepage
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
