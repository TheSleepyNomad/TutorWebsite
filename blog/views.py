import re
from turtle import title
from django.shortcuts import render
from .models import Article, Gallery, Tag, Category
from landingpage.views import is_fetch
from django.http import JsonResponse
from datetime import datetime
# Create your views here.
def blog_list(request):
    if is_fetch(request):
        if len(request.FILES) > 1:
            for img in range(1, len(request.FILES)):
                image = request.FILES.get(f'gallary{img}')
                time = datetime.now()
                gallery = Gallery(title=f'gallery-{time.strftime("%d-%m-%Y %H:%M")}', image=image)
                gallery.save()
        article = Article(
            title=request.POST.get('title'),
            entry_image=request.FILES.get('entry-img'),
            text=request.POST.get('text'),
            category=Category.objects.get(pk=request.POST.get('category')),
        )
        article.save()
        article.tags.set(Tag.objects.filter(pk__in=request.POST.get('tag')))
        return JsonResponse({'status':'200', 'ok': True})
    return render(request,'blog/blog.html')

def blog_detail(request, pk):
    article = Article.objects.get(pk=pk)
    return render(request,'blog/blog_detail.html', context={"article" : article})