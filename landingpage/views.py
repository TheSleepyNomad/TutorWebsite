from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.conf import settings
from django.core.mail import send_mail
# Мои функции
from landingpage.services import is_fetch


class LandingPageView(TemplateView):
    template_name = "landingpage/index.html"

    def post(self, request, *args, **kwargs):
        if is_fetch(request):
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
                return JsonResponse({'status':'200', 'ok': True})

        return self.get(request, *args, **kwargs)
    
