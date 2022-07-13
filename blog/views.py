import re
from django.shortcuts import render
from .models import Article

# Create your views here.
def blog_list(request):
    return render(request,'blog/blog.html')

def blog_detail(request, pk):
    article = Article.objects.get(pk=pk)
    return render(request,'blog/blog_detail.html', context={"article" : article})