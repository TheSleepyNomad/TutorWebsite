from django.shortcuts import render
from .models import Article, Gallery, Tag, Category
from landingpage.views import is_fetch
from django.http import JsonResponse
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models import Count

# ? Рендер страницы с статьями, обработка CMS формы для добавления статей + сортировка и поиск
# Todo Переписать на cbv перед деплоем
#   Подумать над реализацией поиска на клиентской части через API
def blog_list(request):
    print(request.GET)
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
            prev_text=request.POST.get('prev_text'),
            entry_image=request.FILES.get('entry-img'),
            text=request.POST.get('text'), # Хранит в себе html разметку, которая генирируется на стороне клиента
            category=Category.objects.get(pk=request.POST.get('category')), # Todo Почитать документацию Django, возможно можно реализовать менее затратно
        )
        article.save()

        # ? Из-за отношения ManyToMany пришлось сохранить объект, чтобы появился id и только после этого связать их
        article.tags.set(Tag.objects.filter(pk__in=request.POST.getlist('tag')))

        # Todo не забыть про обработку ошибок и исключений!
        return JsonResponse({'status':'200', 'ok': True})
    
    # Обработка поискового запроса
    search_article = request.GET.get('search')
    category_article = request.GET.get('category')
    # Поиск через форму поиска
    if search_article:
        articles_list = Article.objects.filter(\
            Q(title__icontains=search_article)\
            | Q(prev_text__icontains=search_article)\
            | Q(prev_text__icontains=search_article.title())\
            | Q(title__icontains=search_article.title()))\
            .only('title', 'prev_text', 'entry_image', 'created_at').order_by('-id')
    # Поиск по категориями
    if category_article:
        articles_list = Article.objects.filter(category__name=category_article).only('title', 'prev_text', 'entry_image', 'created_at').order_by('-id')
    else:
        articles_list = Article.objects.all()\
            .only('title', 'prev_text', 'entry_image', 'created_at').order_by('-id')

    paginator = Paginator(articles_list, 5) # Количество постов на странице
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    
    context = {
        'page': page,
        'articles': articles,
        'tags': Tag.objects.all().values_list('id', 'name'),
        'category': Category.objects.all().values_list('id', 'name').annotate(article_count=Count('article'))
        }
    return render(request,'blog/blog.html', context=context)


def blog_detail(request, pk):
    
    context = {
        'article': Article.objects.get(pk=pk),
        'tags': Tag.objects.all().values_list('id', 'name'),
        'category': Category.objects.all().values_list('id', 'name').annotate(article_count=Count('article'))
    }
    return render(request,'blog/blog_detail.html', context=context)