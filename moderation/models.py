from django.db import models


class BannedWord(models.Model):
    banned_word = models.CharField(max_length=100)

    def __str__(self):
        return self.banned_word


class Referral(models.Model):
    ref_list = models.CharField(max_length=20)

    def __str__(self):
        return self.ref_list