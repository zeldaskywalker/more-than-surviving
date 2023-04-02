from django.db import models

class Image(models.Model):
    image_id = models.CharField(max_length=50, primary_key=True)
    url = models.URLField()
    alt_text = models.CharField(max_length=100)
    caption = models.CharField(max_length=100)
    credit = models.CharField(max_length=100)

    def __str__(self):
        return self.image_id


class Event(models.Model):
    class DateAccuracy(models.TextChoices):
        DAY = 'DAY', ('Day')
        MONTH = 'MONTH', ('Month')
        YEAR = 'YEAR', ('Year')

    eventid = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=100)
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
    issue_types = models.URLField()
    short_description = models.CharField(max_length=100)
    long_description = models.CharField(max_length=300)
    citations = models.CharField(max_length=300)
    activist_ids = models.JSONField()
    related_event_ids = models.JSONField()
    image_ids = models.JSONField()
    thumbnail_link = models.URLField()
    location_names = models.JSONField()
    location_data = models.JSONField()


class Activist(models.Model):
    class DateAccuracy(models.TextChoices):
        DAY = 'DAY', ('Day')
        MONTH = 'MONTH', ('Month')
        YEAR = 'YEAR', ('Year')

    activist_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    event_ids = models.JSONField()
    image_ids = models.JSONField()
    tribal_affiliations = models.JSONField()
    date_of_birth = models.DateField()
    date_of_birth_accuracy = models.CharField(
        max_length=5,
        choices=DateAccuracy.choices,
        default=DateAccuracy.YEAR,
    )
    longitude_of_birth = models.DecimalField(max_digits=9, decimal_places=6)
    latitude_of_birth = models.DecimalField(max_digits=9, decimal_places=6)
    date_of_death = models.DateField()
    date_of_death_accuracy = models.CharField(
        max_length=5,
        choices=DateAccuracy.choices,
        default=DateAccuracy.YEAR,
    )
    short_bio = models.CharField(max_length=100)
    long_bio = models.CharField(max_length=300)
    citations = models.CharField(max_length=250)
