from django.contrib import admin
from django.db import models


class Users(models.Model):
    name = models.CharField(max_length=50)
    mail_address = models.EmailField()
    password = models.CharField(max_length=20)

    class Meta:
        db_table = 'users'


class Videos(models.Model):
    name = models.CharField(max_length=100)
    year_of_issue = models.IntegerField()
    country = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    duration = models.IntegerField()
    premiere = models.CharField(max_length=50)
    description = models.TextField()
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/')
    type = models.CharField(max_length=30)
    season = models.SmallIntegerField(null=True, blank=True)
    last_episode = models.SmallIntegerField(null=True, blank=True)
    label = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        db_table = 'videos'


class UserSubscriptions(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    video = models.ForeignKey(Videos, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_subscriptions'


class Websites(models.Model):
    title = models.TextField()
    video = models.ForeignKey(Videos, on_delete=models.CASCADE)
    update_date = models.CharField(max_length=50)
    link_to_watch_online = models.URLField()
    quality = models.CharField(max_length=50)
    translation = models.CharField(max_length=100)

    class Meta:
        db_table = 'websites'


admin.site.register(Users)
admin.site.register(Videos)
admin.site.register(UserSubscriptions)
admin.site.register(Websites)





