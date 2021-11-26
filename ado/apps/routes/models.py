from django.db import models
from ado.apps.buses.models import Bus


class Route(models.Model):
    name = models.CharField(max_length=155)
    schedule = models.DateTimeField()
    buses = models.ManyToManyField(Bus)

    class Meta:
        verbose_name = "Route"
        verbose_name_plural = "Routes"

    def __str__(self) -> str:
        return self.name
