from turtle import title
from django.shortcuts import render
from .models import Article, Gallery, Tag, Category
from landingpage.views import is_fetch
from django.http import JsonResponse
from datetime import datetime


# * @TheSleepyNomad
# ? Рендер страницы с статьями, обработка CMS формы для добавления статей + сортировка и поиск
# Todo Переписать на cbv перед деплоем
#   Подумать над реализацией поиска на клиентской части через API
def blog_list(request):

    # Обработка запросов от формы добавления статей
    if is_fetch(request):
        # Если запросе есть файлы кроме главного баннера, то эти файлы идут в галлерею 
        if len(request.FILES) > 1:
            for img in range(1, len(request.FILES)):
                image = request.FILES.get(f'gallary{img}')
                time = datetime.now()
                gallery = Gallery(title=f'gallery-{time.strftime("%d-%m-%Y %H:%M")}', image=image)
                gallery.save()

        article = Article(
            title=request.POST.get('title'),
            entry_image=request.FILES.get('entry-img'),
            text=request.POST.get('text'), # Хранит в себе html разметку, которая генирируется на стороне клиента
            category=Category.objects.get(pk=request.POST.get('category')), # Todo Почитать документацию Django, возможно можно реализовать менее затратно
        )
        article.save()

        # ? Из-за отношения ManyToMany пришлось сохранить объект, чтобы появился id и только после этого связать их
        article.tags.set(Tag.objects.filter(pk__in=request.POST.get('tag')))

        # Todo не забыть про обработку ошибок и исключений!
        return JsonResponse({'status':'200', 'ok': True})
    return render(request,'blog/blog.html')


def blog_detail(request, pk):
    article = Article.objects.get(pk=pk)
    return render(request,'blog/blog_detail.html', context={"article" : article})