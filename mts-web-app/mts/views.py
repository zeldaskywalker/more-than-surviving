from django.http import HttpResponse
from django.shortcuts import render

from django.views import generic

from .models import Image

class HomeView(generic.TemplateView):
    model = Image
    template_name = 'home.html'

class MapView(generic.TemplateView):
    model = Image
    template_name = 'map.html'

class TimelineView(generic.TemplateView):
    model = Image
    template_name = 'timeline.html'

class GalleryView(generic.TemplateView):
    model = Image
    template_name = 'gallery.html'

class AboutView(generic.TemplateView):
    model = Image
    template_name = 'about.html'