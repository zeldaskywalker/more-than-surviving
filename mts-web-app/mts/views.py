from django.http import HttpResponse
from django.shortcuts import render

from django.views import generic

class HomeView(generic.TemplateView):
    template_name = 'home.html'

class MapView(generic.TemplateView):
    template_name = 'map.html'

class TimelineView(generic.TemplateView):
    template_name = 'timeline.html'

class GalleryView(generic.TemplateView):
    template_name = 'gallery.html'

class AboutView(generic.TemplateView):
    template_name = 'about.html'