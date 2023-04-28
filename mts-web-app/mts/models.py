"""Django models for interacting with MTS database."""
from django.db import models

class Activists(models.Model):
    """Python object for accessing and managing data for Activists."""

    class DateAccuracy(models.TextChoices):
        """Enum for specifying accuracy of date columns."""
        DAY = 'DAY', ('Day')
        MONTH = 'MONTH', ('Month')
        YEAR = 'YEAR', ('Year')

    activist_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    event_ids = models.JSONField()
    image_ids = models.JSONField()
    tribal_affiliation = models.JSONField(blank=True)
    date_of_birth = models.DateField()
    date_of_birth_accuracy = models.CharField(
        max_length=5,
        choices=DateAccuracy.choices,
        default=DateAccuracy.YEAR,
    )
    latitude_of_birth = models.DecimalField(max_digits=9, decimal_places=6)
    longitude_of_birth = models.DecimalField(max_digits=9, decimal_places=6)
    date_of_death = models.DateField()
    date_of_death_accuracy = models.CharField(
        max_length=5,
        choices=DateAccuracy.choices,
        default=DateAccuracy.YEAR,
    )
    short_bio = models.CharField(max_length=10000)
    long_bio = models.CharField(max_length=10000)
    citations = models.CharField(max_length=10000)

    class Meta:
        """DO NOT EDIT."""
        managed = False
        db_table = 'activists'


class Events(models.Model):
    """Python object for accessing and managing data for Events."""

    class DateAccuracy(models.TextChoices):
        """Enum for specifying accuracy of date columns."""
        DAY = 'DAY', ('Day')
        MONTH = 'MONTH', ('Month')
        YEAR = 'YEAR', ('Year')

    event_id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=500)
    map = models.BooleanField()
    start_date = models.DateField()
    start_date_accuracy = models.CharField(
        max_length=5,
        choices=DateAccuracy.choices,
        default=DateAccuracy.YEAR,
    )
    end_date = models.DateField()
    end_date_accuracy = models.CharField(
        max_length=5,
        choices=DateAccuracy.choices,
        default=DateAccuracy.YEAR,
    )
    issue_types = models.JSONField()
    short_description = models.CharField(max_length=10000)
    long_description = models.CharField(max_length=10000)
    citations = models.CharField(max_length=10000)
    activist_ids = models.JSONField()
    related_event_ids = models.JSONField()
    image_ids = models.JSONField()
    location_names = models.JSONField()
    location_data = models.JSONField()

    class Meta:
        """DO NOT EDIT."""
        managed = False
        db_table = 'events'


class Images(models.Model):
    """Python object for accessing and managing data for Images."""

    image_id = models.CharField(max_length=50, primary_key=True)
    header_url = models.URLField()
    timeline_url = models.CharField(max_length=10000)
    alt_text = models.CharField(max_length=10000)
    caption = models.CharField(max_length=10000)
    credit = models.CharField(max_length=10000)

    class Meta:
        """DO NOT EDIT."""
        managed = False
        db_table = 'images'
