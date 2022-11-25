from django.db import models


class BannedList(models.Model):
    banned_word = models.CharField(max_length=100)

    def __str__(self):
        return self.banned_word