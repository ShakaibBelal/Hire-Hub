from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .models import Company, Candidates
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from .forms import *
from django.db import IntegrityError
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        candidates=Candidates.objects.all()
        context={
            'candidates':candidates,
        }
        if request.user.is_superuser:
            return render(request,'hr.html',context)
        else:
            companies=Company.objects.all()
            context={
                'companies':companies,
            }
            return render(request,'Jobseeker.html',context)
    else:
        companies=Company.objects.all()
        context={
            'companies':companies,
        }
        return render(request,'Jobseeker.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    else:
       if request.method=="POST":
        name=request.POST.get('username')
        pwd=request.POST.get('password')
        user=authenticate(request,username=name,password=pwd)
        if user is not None:
            login(request,user)
            return redirect('home')
       return render(request,'login.html')
    
def registerUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Create a new user
        user = User.objects.create_user(username, email, password)

     
        

        # Redirect to the home page
        return redirect('login')

    return render(request, 'register.html')

def applyPage(request):
    if request.user.is_anonymous:
        return redirect('login')  
    company = Company.objects.all()
    if request.method=='POST':
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        resume = request.POST.get('resume')
        gender = request.POST.get('gender')
        company_name = request.POST.get('company')
        companyy = Company.objects.get(name=company_name)

        candidate = Candidates.objects.create(
           name = name,
           dob = dob,
           email = email,
           mobile = mobile,
           resume = resume,
           gender = gender,
           company = companyy
        )
        candidate.save()

    
        context={
            'company': company
        }
        return render(request,'apply.html',context)
    context={
            'company': company
    }
    return render(request,'apply.html', context)

class AddCompany(LoginRequiredMixin,CreateView):
  model=Company
  fields='__all__'
  success_url=reverse_lazy(home)
  login_url = '/login/'

def user_info(request):
    user =Company.objects.all()
    context = {
        'user': user,
       }
    return render(request, 'user_info.html', context)
def view_candidates(request, company_id=None):
    
    if not company_id:
        company_id = request.user.company.id
    
    company = get_object_or_404(Company, id=company_id)
    candidates = Candidates.objects.filter(company=company)
   
    
    # Filter candidates based on the user's company id
    user_candidates = [candidate for candidate in candidates if candidate.company_id == company_id]
    
    return render(request, 'candidate_list.html', {'company': company, 'candidates': user_candidates})

def admin(request):
    return redirect("admin/")
