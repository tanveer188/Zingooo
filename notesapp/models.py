from django.db import models

# Create your models here.
class NotesDb(models.Model):
  f_title = models.CharField(max_length=122)
  f_location = models.CharField(max_length=122)
  def __str__(self):
        return self.f_title