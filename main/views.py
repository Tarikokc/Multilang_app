from django.shortcuts import render, get_object_or_404
from .models import Article
from django.utils.translation import activate
from django.http import HttpResponseRedirect
from django.conf import settings  # Importer le module settings
from django.urls import reverse
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import logging
# Create your views here.
logger = logging.getLogger(__name__)

# retourne la vue de la liste des articles
def all_articiles(request) : 
    """
    Retourne la page listant tous les articles de blog.

    Args:
        request (HttpRequest): L'objet de requête HTTP.

    Returns:
        HttpResponse: Une réponse HTTP contenant le rendu du template 'articles_all.html' avec le contexte.
    """
    articles = Article.objects.all()
    return render(request, 'main/articles_all.html', {'articles': articles, 'LANGUAGES': settings.LANGUAGES})
# retourne le détail d'un article
def article_detail(request, article_id):  
    """
    Retourne la page de détail d'un article spécifique.

    Args:
        request (HttpRequest): L'objet de requête HTTP.
        article_id (int): L'ID de l'article à afficher.

    Returns:
        HttpResponse: Une réponse HTTP contenant le rendu du template 'article_detail.html' avec le contexte.
    """
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'main/article_detail.html', {'article': article})

# permet le changement de langue
def change_language(request):
    """
    Change la langue active de l'utilisateur et redirige vers la page précédente.

    Args:
        request (HttpRequest): L'objet de requête HTTP contenant le paramètre 'lang' pour la nouvelle langue.

    Returns:
        HttpResponseRedirect: Une redirection vers la page précédente ou la page d'accueil.
    """
    selected_language = request.GET.get('lang')
    if selected_language and selected_language in [lang[0] for lang in settings.LANGUAGES]:
        activate(selected_language)
        response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Rediriger vers la page précédente ou la page d'accueil
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, selected_language)
        return response
    else:
        return HttpResponseRedirect(reverse('article_list'))

@csrf_exempt
def chatbot(request):
    """
    Gère les interactions avec le chatbot OpenAI.

    Args:
        request (HttpRequest): La requête HTTP, qui peut être de type GET (pour charger la page initiale) ou POST (pour envoyer un message au chatbot).

    Returns:
        HttpResponse ou JsonResponse:
            - Si la requête est GET, renvoie une réponse HTTP avec le rendu du template 'main/chatbot.html'.
            - Si la requête est POST, renvoie une réponse JSON contenant la réponse du chatbot ou un message d'erreur.
    """
    if request.method == 'POST':
        try:
            user_input = request.POST.get('user_input')
            logger.info(f"User input: {user_input}")

            openai.api_key = settings.OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input},
                ]
            )
            assistant_response = response.choices[0].message['content']
            logger.info(f"Assistant response: {assistant_response}")

            return JsonResponse({'response': assistant_response})
        except Exception as e:
            logger.error(f"Error: {str(e)}", exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)
    return render(request, 'main/chatbot.html')
