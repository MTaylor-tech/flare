
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import *

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'lore/index.html'
    context_object_name = 'latest_lore_list'

    def get_queryset(self):
        return LoreArticle.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = LoreArticle
    template_name = 'lore/detail.html'

    def get_queryset(self):
        return LoreArticle.objects.filter(pub_date__lte=timezone.now())
