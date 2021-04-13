from django.db import models

# Create your models here.
class Usuario(models.Model):
    correo=models.EmailField()
    timestamp=models.DateTimeField(auto_now_add=True)
    temperatura=models.FloatField()
    oxigenacion=models.IntegerField()
    positivo=models.BooleanField()

    def __str__(self):
        return self.correo