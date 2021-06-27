from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=64)
    role = models.CharField(
        choices=[
            ("interviewer", "Interviewer"),
            ("candidate", "Candidate"),
        ],
        max_length=16,
    )


class AvailabilitySlot(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    time = models.DateTimeField()

    class Meta:
        unique_together = [("person", "time")]


class Interview(models.Model):
    """Scheduled interview"""
    persons = models.ManyToManyField(Person)
    time = models.DateTimeField()
