from django.db import models


class WarningText(models.Model):
    warning_text = models.CharField(max_length=150, blank=True)
    warning_number = models.IntegerField('Warnings max before banning user', default=3)

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


class Rule(models.Model):
    rules_text = models.TextField()
    active = models.BooleanField('active message', default=False)

    def __str__(self):
        return self.rules_text


class WelcomeMessage(models.Model):
    welcome_text = models.TextField()
    active = models.BooleanField('active welcome', default=False)

    def __str__(self):
        return self.welcome_text


class Quote(models.Model):
    text = models.CharField(max_length=255)
    author = models.CharField(max_length=50, default="")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.text