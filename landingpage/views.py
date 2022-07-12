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
    """
    Отвечает за рендер главной страницы - landing page
    """

    # обработка формы контактной связи
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
            return JsonResponse({'status':'500', 'ok': False})

        finally:

            #? Для разработки клиентской части будем симулировать успешную отправку
            return JsonResponse({'status':'200', 'ok': True})

    return render(request, 'landingpage/index.html')