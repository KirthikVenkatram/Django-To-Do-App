from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import TodoForm, UserRegisterForm
from .models import Todo

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('base')  # Change this to the appropriate URL
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'task/login.html')

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'task/register.html', {'form': form})

def home(request):
    context = {'todos' : Todo.objects.all().order_by('-created_date')}
    return render(request, 'task/home.html', context)

def create_todo(request):
    if request.method == 'POST':
        forms = TodoForm(request.POST)
        if forms.is_valid():
            forms.save()
            messages.success(request,'Your Todo is created!')
            return redirect('home')
    else:
        forms = TodoForm()

    context = {
        'form':forms
    }
    return render(request, 'task/create.html', context)

def edit_todo(request, pk):
    if request.method == 'POST':
        todo = Todo.objects.get(id=pk)
        forms = TodoForm(request.POST)
        if forms.is_valid():
            todo.title = forms.instance.title
            todo.task_content = forms.instance.task_content
            todo.save()
            messages.success(request,'Your Todo is Updated Successfully!')
            return redirect('home')
    else:
        todo = Todo.objects.get(id=pk)
        forms = TodoForm(instance=todo)
    return render(request, 'task/edit.html', {'form':forms})

def complete(request, pk):
    todo = Todo.objects.get(id=pk)
    todo.complete = True
    todo.save()
    context = {'todos' : Todo.objects.all()}
    return render(request, 'task/home.html', context)

def delete(request, pk):
    todo = Todo.objects.get(id=pk)
    todo.delete()
    context = {'todos' : Todo.objects.all()}
    return render(request, 'task/home.html', context)

def completed(request):
    todo = Todo.objects.all().filter(complete=True)
    context = {'todos' : todo}
    return render(request, 'task/completed.html', context)

def user_logout(request):
    logout(request)
    return redirect('home')
