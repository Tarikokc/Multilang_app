from django.urls import path
from . import views

# Gère les URL des vues
urlpatterns = [
    path('', views.all_articiles, name='articles'),
    path('<int:article_id>/', views.article_detail, name='article_detail'),
    path('change_language/', views.change_language, name='change_language'),
    path('chatbot/', views.chatbot, name='chatbot'),

]