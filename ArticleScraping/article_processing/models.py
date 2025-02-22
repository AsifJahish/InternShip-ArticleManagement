from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models

class ExtractedData(models.Model):
    article = models.ForeignKey('article_upload.Article', on_delete=models.CASCADE)
    year = models.IntegerField()
    country = models.CharField(max_length=100)
    journal = models.CharField(max_length=255)
    article_link = models.URLField()

    def __str__(self):
        return f"{self.article.name} - {self.journal}"
