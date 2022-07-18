from django.shortcuts import render
from .models import Article, Gallery, Tag, Category
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Count
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from landingpage.services import is_fetch


class BlogsListView(ListView):
    model = Article
    paginate_by = 5
    queryset = Article.objects.all().only('title', 'prev_text', 'entry_image', 'created_at').order_by('-id')
    context_object_name = 'Articles'
    template_name = 'blog/blog.html'

    def post(self, request, *args, **kwargs):
        # Проверяем на fetch/ajax запрос
        # На этой старнице только одна форма для добавления статей
        if is_fetch:
            # Если количество отправленных файлов в пакете более 1, значит были файлы добавленные в саму статью
            if len(request.FILES) > 1:
                # Проходимся по полученным файлам, проверяем на существование и создаем по необходимости
                for img in range(1, len(request.FILES)):
                    image = request.FILES.get(f'gallary{img}')
                    if Gallery.objects.filter(prefix='other', image='images/' + str(image)).exists():
                        pass
                    else:
                        gallery_image = Gallery.objects.create(prefix='other', image=image)
                        gallery_image.save()
            # Проверяем картинку-баннер
            if Gallery.objects.filter(prefix='entery', image='images/' + str(request.FILES.get('entry-img'))).exists():
                entry_image = Gallery.objects.get(prefix='entery', image='images/' + str(request.FILES.get('entry-img')))
            else:
                entry_image = Gallery.objects.create(prefix='entery', image=request.FILES.get('entry-img'))
            # Создаем новую статью
            article = Article(
            title=request.POST.get('title'),
            prev_text=request.POST.get('prev_text'),
            entry_image=entry_image,
            text=request.POST.get('text'), # Хранит в себе html разметку, которая генирируется на стороне клиента
            category=Category.objects.get(pk=request.POST.get('category')), # Todo Почитать документацию Django, возможно можно реализовать менее затратно
            )
            article.save()
            # Так как отношение ManyToMany, то использует set и проходимся по списку id тэгов
            article.tags.set(Tag.objects.filter(pk__in=request.POST.getlist('tag')))
            return JsonResponse({'status':'200', 'ok': True})
        return self.get(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        # Обработка фильтров для статей
        search_article = request.GET.get('search')
        category_article = request.GET.get('category')
        tag_article = request.GET.get('tag')
        # Через форму поиска
        if search_article:
            # Поиск идет по превью тексту и заголовку
            self.queryset = Article.objects.filter(\
                Q(title__icontains=search_article)\
                | Q(prev_text__icontains=search_article)\
                | Q(prev_text__icontains=search_article.title())\
                | Q(title__icontains=search_article.title()))\
                .only('title', 'prev_text', 'entry_image', 'created_at').order_by('-id')
        if tag_article:
            self.queryset = Article.objects.filter(\
                Q(tags__name=tag_article)\
                | Q(tags__name=tag_article.title()))\
                .only('title', 'prev_text', 'entry_image', 'created_at').order_by('-id')
        if category_article:
            self.queryset = Article.objects.filter(category__name=category_article).only('title', 'prev_text', 'entry_image', 'created_at').order_by('-id')

        return super().get(request, *args, **kwargs)


    def get_context_data(self,*args, **kwargs):
        context = super(BlogsListView,self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all().values_list('id', 'name')
        context['category'] = Category.objects.all().values_list('id', 'name').annotate(article_count=Count('article'))
        context['recrent_articles'] = Article.objects.filter(created_at__date__lt=datetime.now()).only('title', 'entry_image', 'created_at').order_by('-id')[:5]
        return context


class BlogDetailView(DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'blog/blog_detail.html'

    def get_context_data(self,*args, **kwargs):
        context = super(BlogDetailView,self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all().values_list('id', 'name')
        context['category'] = Category.objects.all().values_list('id', 'name').annotate(article_count=Count('article'))
        context['recrent_articles'] = Article.objects.filter(created_at__date__lt=datetime.now()).only('title', 'entry_image', 'created_at').order_by('-id')[:5]
        return context
