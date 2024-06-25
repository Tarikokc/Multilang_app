from django.contrib import admin
from .models import Article
from modeltranslation.admin import TranslationAdmin
from . import translation  # Importez le module translation ici

# Panel ADMIN pour les modèles
@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    pass