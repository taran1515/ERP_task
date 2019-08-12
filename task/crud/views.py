from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .forms import UserForm,UserProfileInfoForm,UpdateUserProfileInfoForm
from .models import User,UserProfileInfo
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse

from django.contrib.auth.decorators import login_required
n = 0
def index(request):

    alluser = UserProfileInfo.objects.all()
    countuser = UserProfileInfo.objects.count()
    context = {
        'alluser':alluser,
        'countuser':countuser
    }
    return render(request,'crud/index.html',context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('crud:index'))

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                # print(user)
                clg_name = UserProfileInfo.objects.get(user=user)
                return render(request,'crud/index.html',{
                    'clg_name':clg_name.college_name,
                })
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed")
            print("Username:{} and password {}".format(username,password))
            return HttpResponse("Invalid credentials")
    else:
        return render(request,'crud/login.html',{})


def update(request):

    update = False
    if request.user.is_authenticated:
        if request.user.is_active:

            if request.method == "POST":
                update_form = UpdateUserProfileInfoForm(data=request.POST)
                if update_form.is_valid():

                    #
                    # user = update_form.save(commit=False)
                    newuser = UserProfileInfo.objects.get(user=request.user)
                    x=newuser.user
                    newuser.college_name = request.POST['college_name']
                    print(newuser.college_name)
                    # newuser.college_name.value.save()
                    newuser.save()
                    update = True

            else:

                update_form = UpdateUserProfileInfoForm()
                newuser = UserProfileInfo.objects.get(user=request.user)
            return render(request,'crud/update.html',{
                'update':update,
                'update_form':update_form,
                'newuser':newuser,


    })


def delete(request):

    delete = True
    if request.user.is_authenticated:
        if request.user.is_active:

            if delete:
                newuser = UserProfileInfo.objects.get(user=request.user)
                newuser.college_name=None
                newuser.save()

            return render(request,'crud/delete.html',{
                'delete':delete,
                'newuser':newuser,
            })


def register(request):

    registered=False

    if request.method =="POST":
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() :

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit = False)
            profile.user = user
            profile.save()


            registered = True

        else:

            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()


    return render(request,'crud/registration.html',
                  {'user_form':user_form,
                   'profile_form': profile_form,
                   'registered':registered})

