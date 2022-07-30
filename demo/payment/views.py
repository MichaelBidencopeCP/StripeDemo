from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
import os
import dotenv
import json
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)




end_point_secret = os.getenv('STRIPE_SIG')




# Create your views here.
def login_page(request):
    
    if request.user.is_authenticated:
        return redirect('/payment')
    #check for post request
    if request.method == 'POST':
        if 'username1' in request.POST.keys() and 'password' in request.POST.keys():
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

def secret(request, plan):
    stripe.api_key = os.getenv('STRIPE_PRIVATE_TOKEN')
    intent = stripe.PaymentIntent.create(
        amount= 1000 if plan == 0 else 2000,
        currency="usd",
        automatic_payment_methods={"enabled": True},
    )
    
    client_secret = {'secret':intent['client_secret']}

    return JsonResponse(client_secret)
@csrf_exempt
def paymentsAPI(request):

    if request.method == 'POST':
        data = request.POST
        try:
            event = json.loads(data)
        except:
            print('Webhook error while parsing basic request.' + str(e))
            return JsonResponse(success=False)
        if end_point_secret:
            # Only verify the event if there is an endpoint secret defined
            # Otherwise use the basic event deserialized with json
            sig_header = request.headers.get('stripe-signature')
            try:
                event = stripe.Webhook.construct_event(
                    data, sig_header, end_point_secret
                )
            except stripe.error.SignatureVerificationError as e:
                print('Webhook signature verification failed.' + str(e))
                return JsonResponse(success=False)
        if event and event['type'] == 'payment_intent.succeeded':
            print('Webhook received!')
            print(event)

            return JsonResponse(success=True)

