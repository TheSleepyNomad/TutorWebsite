from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail


def is_fetch(request):
    """
    Функциая проверяет запрос на наличия заголовка, который подскажет что это отправили через ajax или fetch
    """

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return True


def index(request):
    if is_fetch(request):
        # !Todo проверить работу почты на хостинге
        # Отправка почты
        try:
            send_mail(
                request.POST['subject'], # Тема
                request.POST['message'], # Текст письма
                settings.EMAIL_HOST_USER, # От кого
                ['iluxaan@mail.ru',], # Кому
            )

        except Exception:
            pass

        finally:

        #? Для разработки клиентской части будем симулировать успешную отправку
            return JsonResponse({'status':'200'})
            
    return render(request, 'landingpage/index.html')