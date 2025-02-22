from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import ExtractedData
from article_upload.models import Article
import PyPDF2
import re

def extract_data(request):
    articles = Article.objects.all()
    for article in articles:
        with open(article.file.path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = " ".join(page.extract_text() for page in reader.pages if page.extract_text())

            # Extract Data Using Simple Regex (You can improve this)
            year = re.search(r"\b(19|20)\d{2}\b", text)
            country = re.search(r"(Kazakhstan|USA|Canada|UK|India)", text)
            journal = re.search(r"Journal of [A-Za-z\s]+", text)

            ExtractedData.objects.update_or_create(
                article=article,
                defaults={
                    "year": int(year.group()) if year else 2000,
                    "country": country.group() if country else "Unknown",
                    "journal": journal.group() if journal else "Unknown Journal",
                    "article_link": f"/media/{article.file}"
                }
            )
    
    extracted_data = ExtractedData.objects.all()
    return render(request, 'extracted_data.html', {'extracted_data': extracted_data})
