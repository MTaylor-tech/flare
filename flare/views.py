from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'flare/index.html'

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)
