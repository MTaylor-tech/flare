from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import *
from skill.models import *
from .forms import *
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

class CharacterSkillsCreate(LoginRequiredMixin, CreateView):
    model = Character_Skill
    fields = ['multiplier','skill','option']

class CharacterCreate(LoginRequiredMixin, CreateView):
    model = Character
    fields = ['name','character_class','character_race','character_subrace']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'character/index.html'
    context_object_name = 'user_character_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Character.objects.filter(user=self.request.user)
        else:
            return None

class AdminView(generic.ListView):
    template_name = 'character/index.html'
    context_object_name = 'user_character_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.profile.is_admin:
                return Character.objects.all()
            else:
                return Character.objects.filter(user=self.request.user)
        else:
            return None

class DetailView(generic.DetailView):
    model = Character
    template_name = 'character/detail.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.profile.is_admin:
                return Character.objects.all()
            else:
                return Character.objects.filter(user=self.request.user)
        else:
            return Character.objects.all()

class BuySkillsView(generic.DetailView):
    model = Character
    template_name = 'character/buyskills.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return Skill.objects.all()

def save(request, character_id):
    if request.method == 'POST':
        character = get_object_or_404(Character, pk=character_id)
        character.name = request.POST['name']
        character.player_notes = request.POST['player_notes']
        character.bio = request.POST['bio']
        try:
            value = request.POST['remove_image']
            character.image = ''
        except:
            pass
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if (request.FILES['image']):
                character.image = request.FILES['image']
        character.save()
        return HttpResponseRedirect(reverse('character:detail', args=(character.id,)))
    else:
        return HttpResponseForbidden('Forbidden action. This action is only permitted as a form submission.')
