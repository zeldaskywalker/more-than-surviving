from django.http import HttpResponse
from django.shortcuts import render

from django.views import generic

from .models import Activists, Events, Images

class HomeView(generic.TemplateView):
    template_name = 'home.html'

class MapView(generic.TemplateView):
    template_name = 'map.html'

class TimelineView(generic.TemplateView):
    template_name = 'timeline.html'

class GalleryView(generic.TemplateView):
    template_name = 'gallery.html'

class GlossaryView(generic.TemplateView):
    template_name = 'glossary.html'

class AboutView(generic.TemplateView):
    template_name = 'about.html'

class EventView(generic.DetailView):
    model = Events
    template_name = 'event.html'

class ActivistView(generic.DetailView):
    model = Activists
    template_name = 'activist.html'