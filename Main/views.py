from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.http import HttpResponse
from . forms import CreateAccountForm, UpdateAccountForm, CreateJobForm, CreateReportForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from . models import Profile, Post, Report

def create_account(request):
    if request.method == "POST": #user clicks register button
        print('create account post')
        form = CreateAccountForm(request.POST)

        if form.is_valid():
            print('create account valid')

            #get form data
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']

            #create and add user to database
            user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
            user.set_password(password)
            profile = Profile.objects.create(User=user, Age=age)

            user.save()
            profile.save()
            login(request, user)
            
            return redirect('/home/')

    else: #user is viewing the create account page
        form = CreateAccountForm()

    return render(request, 'createAccount.html', {'form':form})


def profile(request):
    return render(request, 'profile.html')
    #return HttpResponse("profile.")


#TODO: change to update profile
def update_account(request):
    #TODO: check if user is logged in

    if request.method == 'POST':
        print('update account post')
        form = UpdateAccountForm(request.POST)

        if form.is_valid():
            print('update account valid')
            update_all = 'update_all_button' in request.POST

            if form.cleaned_data['profile_picture'] and ('profile_picture_button' in request.POST or update_all):
                request.user.profile.ProfilePicture = form.cleaned_data['profile_picture'] 

            if form.cleaned_data['first_name'] and ('first_name_button' in request.POST or update_all):
                request.user.first_name = form.cleaned_data['first_name']

            if  form.cleaned_data['last_name'] and ('last_name_button' in request.POST or update_all):
                request.user.last_name = form.cleaned_data['last_name']

            if form.cleaned_data['age'] and ('age_button' in request.POST or update_all):
                request.user.profile.Age = form.cleaned_data['age']

            if form.cleaned_data['email'] and ('email_button' in request.POST or update_all):
                request.user.email = form.cleaned_data['email']

            if form.cleaned_data['description'] and ('description_button' in request.POST or update_all):
                request.user.profile.Description = form.cleaned_data['description']

            if (form.cleaned_data['password'] and form.cleaned_data['password_confirmation']) and ('password_button' in request.POST or update_all):
                request.user.set_password(form.cleaned_data['password'])

            request.user.save()
            request.user.profile.save()

            return render(request, 'updateAccount.html')
    else:
        form = UpdateAccountForm()

    return render(request, 'updateAccount.html', {'form': form})

#home page
def home(request):
    return render(request, 'home.html')
    #return HttpResponse("home.")

def login_request(request):
    if request.method == 'POST':
        print('login post')
        form = AuthenticationForm(request=request, data=request.POST)

        if form.is_valid():
            print('login valid')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/home/')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form':form})

#redirect to home    
def logout_request(request):
    logout(request)
    return redirect('/home/')

#create_job page
def create_job(request):
    if request.method == 'POST':
        print('create job post')
        form = CreateJobForm(request.POST)

        if form.is_valid():
            print('create job valid')
            #get form fields
            pay = form.cleaned_data['pay']
            date = form.cleaned_data['date_time']
            description = form.cleaned_data['description']
            job_type = form.cleaned_data['job_type']

            #create new job
            Post.objects.create(Pay=pay, DateTime=date, Description=description, JobType=job_type)

            return redirect('/add_job/')
    else:
        form = CreateJobForm()

    return render(request, 'Jobs/bigBoxJob.html', {'form':form})

def create_report(request):
    if request.method == "POST": #?
        print('create report post')
        form = CreateReportForm(request.POST)

        if form.is_valid():
            print('create report valid')

            classification = form.cleaned_data['classification']
            details = form.cleaned_data['details']

            username = request.GET['username']
            user = User.objects.get(username=username) #look out for does not exist exception
            if user is None:
                pass #TODO: add proper error redirecting
            else:
                Report.objects.create(Classification=classification, Details=details, User=user)

            return redirect('/profile/') #TODO: redirect user to the profile that they previously looked at
    else:
        form = CreateReportForm()

    return render(request, 'report.html', {'form':form}) #TODO: add actual html name later


def list_job(request):
    return render(request, 'Jobs/listJobs.html')

def new_job(request):
    return render(request, 'Jobs/viewNewJob.html')

#Job Creator Pages
def all_jobs_creator(request):
    return render(request, 'Creator/allJobsCreator.html')

def accepted_jobs_creator(request):
    return render(request, 'Creator/acceptedJobsCreator.html')

def pending_jobs_creator(request):
    return render(request, 'Creator/pendingJobsCreator.html')

#Jobs Seeker Pages
def all_jobs_seeker(request):
    return render(request, 'Seeker/allJobsSeeker.html')

def accepted_jobs_seeker(request):
    return render(request, 'Seeker/acceptedJobsSeeker.html')

def interested_jobs_seeker(request):
    return render(request, 'Seeker/interestedJobsSeeker.html')