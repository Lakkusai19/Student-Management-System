from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm, TeacherRegistrationForm, StudentUpdateForm
from .models import Profile

def index(request):
    return render(request, 'index.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    return render(request, 'register_student.html', {'form': StudentRegistrationForm()})

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            profile = user.profile
            profile.role = 'teacher'
            profile.employee_id = form.cleaned_data['employee_id']
            profile.save()
            return redirect('login')
    return render(request, 'register_teacher.html', {'form': TeacherRegistrationForm()})

@login_required
def dashboard(request):
    profile = request.user.profile
    if profile.role == 'teacher':
        students = Profile.objects.filter(role='student')
        return render(request, 'teacher_dashboard.html', {'students': students})
    return render(request, 'student_dashboard.html', {'profile': profile})

@login_required
def edit_student(request, id):
    student_profile = get_object_or_404(Profile, id=id)
    form = StudentUpdateForm(request.POST or None, instance=student_profile)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'edit_student.html', {'form': form})

@login_required
def delete_student(request, id):
    get_object_or_404(Profile, id=id).user.delete()
    return redirect('dashboard')

def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def add_student(request):
    if request.user.profile.role != 'teacher':
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            profile = user.profile
            profile.role = 'student'
            profile.save()
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'add_student.html', {'form': form})