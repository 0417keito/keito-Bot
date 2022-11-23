from django.db import models

# Create your models here.
class School_exam(models.Model):
   school_name = models.CharField(max_length=50, blank=True, null=True)
   japanese = models.URLField(blank=True, null=True)
   math = models.URLField(blank=True, null=True)
   science = models.URLField(blank=True, null=True)
   society = models.URLField(blank=True, null=True)
   
   def __str__(self):
      return str(self.school_name)