from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.urls import reverse, reverse_lazy

# Create your views here.
def registration_view(request):
    return render(request, 'users/sign_up.html')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        print(user)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('blog:blog_list'))
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    return render(request, 'users/sign_in.html')