from pyexpat import model
from django.db import models
from django.contrib.auth.models import User, AbstractUser
import statistics

# Created to add additional attributes for the user in case of need.
class UserExtended(AbstractUser):
    pass


class Music (models.Model):
    title = models.CharField(max_length=100)
    singer = models.CharField(max_length=50)
    date_of_post = models.DateField()
    music_file = models.FileField(upload_to='upload/',default='upload/linkin_park_numb.mp3')

    @property
    def rating(self):  # TO BE IMPLEMENTED FOR THE RATING
        """Returns the average rating for a specific Music"""
        ratings = Rating.objects.filter(musics=self)
        rating_list = ratings.values_list("score", flat=True)
        return statistics.mean(rating_list)


class Rating(models.Model):
    musics = models.ManyToManyField(Music, related_name="rate")
    users = models.ManyToManyField(UserExtended)
    score = models.IntegerField()
