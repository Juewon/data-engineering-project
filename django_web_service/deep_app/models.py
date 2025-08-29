from django.db import models

# Create your models here.
class Codezip(models.Model):
    code = models.IntegerField(primary_key=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'deep_app'
        db_table = 'codezip'


class FoodInfoWithTaboo(models.Model):
    food = models.CharField(primary_key=True, max_length=255)
    info = models.TextField(blank=True, null=True)
    ingredient = models.TextField(blank=True, null=True)
    taboo_ingredient = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'deep_app'
        db_table = 'food_info_with_taboo'


class RankReview(models.Model):
    res = models.ForeignKey('RestaurantInfo', models.DO_NOTHING, blank=True, null=True)
    cnt = models.IntegerField(blank=True, null=True)
    code = models.ForeignKey(Codezip, models.DO_NOTHING, db_column='code', blank=True, null=True)
    id = models.BigIntegerField(primary_key=True)

    class Meta:
        managed = False
        app_label = 'deep_app'
        db_table = 'rank_review'


class RestaurantInfo(models.Model):
    addr = models.TextField(blank=True, null=True)
    food = models.ForeignKey(FoodInfoWithTaboo, models.DO_NOTHING, db_column='food', blank=True, null=True)
    store_name = models.TextField(blank=True, null=True)
    tel = models.CharField(max_length=255, blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'deep_app'
        db_table = 'restaurant_info'


class VisitorReview(models.Model):
    id = models.OneToOneField(RestaurantInfo, models.DO_NOTHING, db_column='id', primary_key=True)
    re_visitor = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'deep_app'
        db_table = 'visitor_review'