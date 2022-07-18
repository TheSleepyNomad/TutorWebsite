def is_fetch(request):
    """
    Функциая проверяет запрос на наличия заголовка, который подскажет что это отправили через ajax или fetch
    """

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return True