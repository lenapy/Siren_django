from django.contrib import admin
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from datetime import datetime, timedelta

from siren_proj.managers import UserManager


class User(AbstractBaseUser):
    username = models.CharField(max_length=50)
    login = models.CharField(max_length=50, unique=True)
    mail_address = models.EmailField()
    password = models.CharField(max_length=49)

    objects = UserManager()

    REQUIRED_FIELDS = ('username',)
    USERNAME_FIELD = 'login'

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username

    def get_full_name(self):
        pass

    def get_short_name(self):
        return self.username


class Video(models.Model):
    name = models.CharField(max_length=100)
    year_of_issue = models.IntegerField()
    country = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    duration = models.IntegerField()
    premiere = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField()
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/')
    type = models.CharField(max_length=30)
    season = models.SmallIntegerField(null=True, blank=True)
    last_episode = models.SmallIntegerField(null=True, blank=True)
    label = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        db_table = 'video'

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_subscription'

    def __str__(self):
        return '{}, {}'.format(self.user, self.video)


class Website(models.Model):
    title = models.TextField()
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    update_date = models.CharField(max_length=50)
    link_to_watch_online = models.URLField()
    quality = models.CharField(max_length=50)
    translation = models.CharField(max_length=100)

    class Meta:
        db_table = 'website'

    def __str__(self):
        return '{}'.format(self.title)


class Session(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=36)
    date_expired = models.DateTimeField(default=datetime.now() + timedelta(days=7))

    class Meta:
        db_table = 'session'

admin.site.register(User)
admin.site.register(Video)
admin.site.register(UserSubscription)
admin.site.register(Website)





