from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=50)
    complete = models.BooleanField(default=False)
    
    
    def __str__(self) -> str:
        return self.name