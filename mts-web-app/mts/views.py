from django.http import HttpResponse
from django.shortcuts import render

from django.views import generic

from .models import Activists, Events, Images

from . import json_translation

class HomeView(generic.TemplateView):
    template_name = 'home.html'

class MapView(generic.TemplateView):
    template_name = 'map.html'

class TimelineView(generic.TemplateView):
    events = Events.objects.all()
    images = Images.objects.all()
    
    events_json = json_translation.events_to_timeline_json(events, images)

    template_name = 'timeline.html'

    def get_context_data(self, **kwargs):
        context = super(TimelineView, self).get_context_data(**kwargs)
        context['timeline_json'] = self.events_json
        return context

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