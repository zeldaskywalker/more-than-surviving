from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('map/', views.MapView.as_view(), name='map'),
    path('timeline/', views.TimelineView.as_view(), name='timeline'),
    path('gallery/', views.GalleryView.as_view(), name='gallery'),
    path('glossary/', views.GlossaryView.as_view(), name='glossary'),
    path('about/', views.AboutView.as_view(), name='about'),
]