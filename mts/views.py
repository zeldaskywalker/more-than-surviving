from django.http import HttpResponse
from django.shortcuts import render

from django.views import generic

from .models import Activists, Events, Images

from . import json_translation

class HomeView(generic.TemplateView):
    template_name = 'home.html'

class MapView(generic.TemplateView):
    events = Events.objects.filter(map=True)
    images = Images.objects.all()
    images_dict = json_translation.create_images_dict(images)

    events_geojson = json_translation.events_to_map_geojson(events, images_dict)

    template_name = 'map.html'

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context['map_geojson'] = self.events_geojson
        return context

class TimelineView(generic.TemplateView):
    events = Events.objects.all()
    images = Images.objects.all()
    images_dict = json_translation.create_images_dict(images)
    
    events_json = json_translation.events_to_timeline_json(events, images_dict)

    template_name = 'timeline.html'

    def get_context_data(self, **kwargs):
        context = super(TimelineView, self).get_context_data(**kwargs)
        context['timeline_json'] = self.events_json
        return context

class GalleryView(generic.ListView):
    template_name = 'gallery.html'
    events = Events.objects.filter(map=True)
    activists = Activists.objects.all()
    images = Images.objects.all()
    images_dict = json_translation.create_images_dict(images)

    all_data = json_translation.gallery_view_dict(events, activists, images_dict)
    context_object_name = 'all_data'

    def get_queryset(self, **kwargs):
        return self.all_data

    def get_context_data(self, **kwargs):
        context = super(GalleryView, self).get_context_data(**kwargs)
        context['data'] = self.all_data
        return context

class GlossaryView(generic.TemplateView):
    template_name = 'glossary.html'

class AboutView(generic.TemplateView):
    template_name = 'about.html'

class EventView(generic.DetailView):
    model = Events
    template_name = 'event.html'

    def get_context_data(self, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)
        all_location_names = self.object.location_names
        location_string = ' and '.join(all_location_names)

        start_date = self.object.start_date
        start_date_accuracy = self.object.start_date_accuracy
        final_start_date = json_translation.date_parser(start_date, start_date_accuracy)

        end_date = self.object.end_date
        end_date_accuracy = self.object.end_date_accuracy
        final_end_date = json_translation.date_parser(end_date, end_date_accuracy)

        event_date_string = json_translation.event_date_string(final_start_date, final_end_date)

        images = Images.objects.all()
        images_dict = json_translation.create_images_dict(images)

        # Code for grabbing DB information for related activist cards
        related_activists = Activists.objects.filter(activist_id__in=self.object.activist_ids)
        activist_cards = json_translation.related_activists_dict(related_activists, images_dict)

        # Code for grabbing DB information for related event cards
        related_events = Events.objects.filter(event_id__in=self.object.related_event_ids)
        event_cards = json_translation.related_events_dict(related_events, images_dict)

        event = Events.objects.filter(event_id=self.object.event_id)
        events_geojson = json_translation.events_to_map_geojson(event, images_dict)

        first_image_id = self.object.image_ids[0]
        final_first_image_id = first_image_id.removesuffix('.jpg').removesuffix('.png').removesuffix('webp').removesuffix('.jpeg')

        context['location_names'] = location_string
        context['image_url'] = Images.objects.get(image_id=first_image_id).url
        context['image_id'] = final_first_image_id
        context['event_date_string'] = event_date_string
        context['image_alt_text'] = Images.objects.get(image_id=first_image_id).alt_text
        context['related_events_and_activists'] = event_cards + activist_cards
        context['map_geojson'] = events_geojson
        return context

class ActivistView(generic.DetailView):
    model = Activists
    template_name = 'activist.html'

    def get_context_data(self, **kwargs):
        context = super(ActivistView, self).get_context_data(**kwargs)
        date_of_birth = self.object.date_of_birth
        date_of_birth_accuracy = self.object.date_of_birth_accuracy
        final_date_of_birth = json_translation.date_parser(date_of_birth, date_of_birth_accuracy)

        date_of_death = self.object.date_of_death
        date_of_death_accuracy = self.object.date_of_death_accuracy
        final_date_of_death = json_translation.date_parser(date_of_death, date_of_death_accuracy)

        tribal_affiliations = self.object.tribal_affiliations
        tribal_affiliations_string = ' and '.join(tribal_affiliations)

        images = Images.objects.all()
        images_dict = json_translation.create_images_dict(images)
        related_events = Events.objects.filter(event_id__in=self.object.event_ids)

        event_cards = json_translation.related_events_dict(related_events, images_dict)

        first_image_id = self.object.image_ids[0]
        final_first_image_id = first_image_id.removesuffix('.jpg').removesuffix('.png').removesuffix('webp').removesuffix('.jpeg')

        context['image_url'] = Images.objects.get(image_id=self.object.image_ids[0]).url
        context['image_id'] = final_first_image_id
        context['image_alt_text'] = Images.objects.get(image_id=self.object.image_ids[0]).alt_text
        context['dob'] = final_date_of_birth
        context['dod'] = final_date_of_death
        context['tribal_affiliations'] = tribal_affiliations_string
        context['related_events'] = event_cards

        return context