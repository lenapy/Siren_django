from django.db import models
from django.contrib.auth.hashers import make_password


class UserManager(models.Manager):

    def registration(self, login, password, username, mail_address, ):  # self - model
        password_hash = make_password(password, hasher='md5')
        user = self.create(login=login,
                           password=password_hash,
                           username=username,
                           mail_address=mail_address,
                           )
        user.save()
        return user.pk

    def change_password(self, password, user_id):
        password_hash = make_password(password, hasher='md5')
        user = self.filter(id=user_id)
        user.update(password=password_hash)


