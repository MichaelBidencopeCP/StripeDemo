from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
# Create your views here.
def login_page(request):
    #check for post request
    if request.method == 'POST':
        if request.POST['username1'] and request.POST['password']:
            username = request.POST['username1']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/home')
            else:
                return render(request, 'login.html', {'error': 'Invalid username or password'})
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            login(request, user)
            return redirect('index')
    #creat signup form
    form = UserCreationForm()
    return render(request, 'login.html', {'form': form})

@login_required()
def index(request):
    #get logged in user
    user = request.user.id

    return render(request, 'payment/index.html', {'user': user})

@login_required()
def logout_page(request):
    logout(request)
    return redirect('login_page')

def payment_page(request):
    return render(request, 'payment/payment.html')
    