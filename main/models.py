from django.db import models

# Modele Article qui initialise les champs
class Article(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='./static/main/images/', null=True, blank=True) 

    def __str__(self):
        return self.title
    
