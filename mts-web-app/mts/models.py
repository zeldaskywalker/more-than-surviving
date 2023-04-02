from django.db import models

class Image(models.Model):
    image_id = models.CharField(max_length=50, primary_key=True)
    url = models.URLField()
    alt_text = models.CharField(max_length=100)
    caption = models.CharField(max_length=100)
    credit = models.CharField(max_length=100)

    def __str__(self):
        return self.image_id
