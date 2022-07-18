from django.http import HttpRequest


def is_fetch(request: HttpRequest) -> bool:
    """
    Функциая проверяет запрос на наличия заголовка, который подскажет что это отправили через ajax или fetch
    """
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return True