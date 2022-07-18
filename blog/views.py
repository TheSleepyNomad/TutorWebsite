from django.shortcuts import render
from .models import Article, Gallery, Tag, Category
from django.http import JsonResponse
from datetime import datetime
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
        if is_fetch:
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
            article.tags.set(Tag.objects.filter(pk__in=request.POST.getlist('tag')))
            return JsonResponse({'status':'200', 'ok': True})
        return self.get(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        search_article = request.GET.get('search')
        category_article = request.GET.get('category')
        tag_article = request.GET.get('tag')
        if search_article:
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

def blog_detail(request, pk):
    
    context = {
        'article': Article.objects.get(pk=pk),
        'tags': Tag.objects.all().values_list('id', 'name'),
        'category': Category.objects.all().values_list('id', 'name').annotate(article_count=Count('article'))
    }
    return render(request,'blog/blog_detail.html', context=context)

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
