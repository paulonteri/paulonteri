from django.core.exceptions import ValidationError
from django.db import models


class Company(models.Model):
    name = models.CharField(unique=True, max_length=20)
    logo = models.ImageField()
    website = models.URLField(null=True, blank=True)
    #
    time_added = models.DateTimeField(auto_now_add=True)
    time_last_edited = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    task = models.CharField(unique=True, max_length=50)
    link = models.URLField(null=True, blank=True, help_text="url to public work")  # url to public work
    weight = models.IntegerField(default=0, help_text="level of importance")  # level of importance
    #
    time_added = models.DateTimeField(auto_now_add=True)
    time_last_edited = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.task

    class Meta:
        ordering = ['weight', '-time_last_edited']


class Job(models.Model):
    title = models.CharField(max_length=20)
    LEVEL_CHOICES = [("Intern", "Intern"), ("Contract", "Contract")]
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    tasks = models.ManyToManyField(Task)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_public = models.BooleanField(default=True)  # should it be shown?
    #
    time_added = models.DateTimeField(auto_now_add=True)
    time_last_edited = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def clean(self):
        if self.end_date and (self.start_date > self.end_date):
            raise ValidationError("End date cannot be before start date!")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:

        def get_level():
            if self.level:
                return "(" + self.level + ") "
            else:
                return ""

        return f"{self.title} {get_level()}- {self.company.name}"
