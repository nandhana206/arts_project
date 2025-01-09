from django.db import models

# Event model with category field to distinguish between onstage and offstage events
class Event(models.Model):
    CATEGORY_CHOICES = [
        ('onstage', 'On-stage'),
        ('offstage', 'Off-stage'),
    ]
    
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='offstage')

    def __str__(self):
        return self.name


# Student model with Many-to-Many relationship to Event model
class Student(models.Model):
    name = models.CharField(max_length=100)
    admission_number = models.CharField(max_length=15, unique=True,default=0)
    department = models.CharField(max_length=50,default='')
    events = models.ManyToManyField(Event, blank=True)  # Relation to the Event model

    def __str__(self):
        return self.name





