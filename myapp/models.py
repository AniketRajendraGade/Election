from django.db import models

# Create your models here.
class Data(models.Model):
    Name = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100)
    District = models.CharField(max_length=100)
    Assembly_Constituency = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/')


    def __str__(self):
        return self.Name