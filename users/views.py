from django.shortcuts import render

# Create your views here.
def registration_view(request):
    return render(request, 'users/sign_up.html')

def login_view(request):
    return render(request, 'users/sign_in.html')