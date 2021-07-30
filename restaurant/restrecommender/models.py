from django.db import models

# Create your models here.


class Restaurantdata(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    online_order = models.BigIntegerField(blank=True, null=True)
    book_table = models.BigIntegerField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    votes = models.BigIntegerField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    rest_type = models.TextField(blank=True, null=True)
    cuisines = models.TextField(blank=True, null=True)
    cost = models.BigIntegerField(blank=True, null=True)
    reviews_list = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    number_of_cuisines_offered = models.BigIntegerField(
        db_column='Number_of_cuisines_offered', blank=True, null=True)  # Field name made lowercase.
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    cluster_label = models.BigIntegerField(
        db_column='Cluster Label', blank=True, null=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    mean_rating = models.FloatField(
        db_column='Mean Rating', blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        managed = False
        db_table = 'restaurantdata'
