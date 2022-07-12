from django.shortcuts import render
from django.http import JsonResponse


def is_fetch(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return True
# Create your views here.
def index(request):
    if is_fetch(request):
        print(request.headers.get('x-requested-with'))
        print(request.POST)
        print(request.POST['name'])
        print(type(request.POST['name']))
        return JsonResponse({'status':'200'})
    return render(request, 'landingpage/index.html')