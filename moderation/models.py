from django.db import models


class WarningText(models.Model):
    warning_text = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.warning_text

    class Meta:
        ordering = ['warning_text']


class BannedWord(models.Model):
    warning_text = models.ForeignKey(WarningText, on_delete=models.CASCADE, null=True)
    banned_word = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.banned_word

    class Meta:
        ordering = ['banned_word']