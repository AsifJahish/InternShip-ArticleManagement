from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})

def upload_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'upload_article.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Article
from .forms import ArticleForm  # Create this form for editing articles

def article_detail(request, id):
    """ View, edit, and delete an article from a single page. """
    article = get_object_or_404(Article, id=id)

    if request.method == "POST":
        if "update" in request.POST:
            form = ArticleForm(request.POST, request.FILES, instance=article)
            if form.is_valid():
                form.save()
                return redirect(reverse('article_detail', args=[id]))
        elif "delete" in request.POST:
            article.delete()
            return redirect('article_list')  # Redirect to the article list after deletion
    else:
        form = ArticleForm(instance=article)

    return render(request, 'detail.html', {'article': article, 'form': form})