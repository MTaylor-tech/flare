
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
    template_name = 'rules/index.html'
    context_object_name = 'latest_rules_list'

    def get_queryset(self):
        return RulesArticle.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = RulesArticle
    template_name = 'rules/detail.html'

    def get_queryset(self):
        return RulesArticle.objects.filter(pub_date__lte=timezone.now())
