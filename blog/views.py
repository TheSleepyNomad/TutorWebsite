from django.shortcuts import render
from .models import Article, Gallery, Tag, Category
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Count
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from datetime import datetime


class BlogsListView(ListView):
    model = Article
    paginate_by = 5
    # queryset = Article.objects.all().select_related('entry_image','category').only('title','entry_image__image','text','category__id','category__name').order_by('-id')
    context_object_name = 'articles'
    template_name = 'blog/blog.html'

    def get_queryset(self):
        return super(BlogsListView, self).get_queryset().select_related('entry_image',).only('title', 'prev_text', 'entry_image__image').order_by('-id')

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
        context['recrent_articles'] = Article.objects.filter(created_at__date__lt=datetime.now()).select_related('entry_image').only('title', 'entry_image__image', 'created_at').order_by('-id')[:5]
        return context


class BlogDetailView(DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'blog/blog_detail.html'
    
    def get_queryset(self):
        return Article.objects.select_related('entry_image','category').only('title','entry_image__image','text','category__id','category__name')

    def get_context_data(self,*args, **kwargs):
        context = super(BlogDetailView,self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all().values_list('id', 'name')
        context['category'] = Category.objects.all().values_list('id', 'name').annotate(article_count=Count('article'))
        context['recrent_articles'] = Article.objects.filter(created_at__date__lt=datetime.now()).select_related('entry_image').only('title', 'entry_image__image', 'created_at').order_by('-id')[:5]
        return context
