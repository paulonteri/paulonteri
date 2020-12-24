from django.core.exceptions import ValidationError
from django.db import models


class Category(models.Model):
    name = models.CharField(unique=True, max_length=20)
    image = models.ImageField(null=True, blank=True)
    slug = models.SlugField()
    #
    time_added = models.DateTimeField(auto_now_add=True)
    time_last_edited = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(unique=True, max_length=20)
    categories = models.ManyToManyField(Category)
    image = models.ImageField(null=True, blank=True)
    slug = models.SlugField()
    #
    time_added = models.DateTimeField(auto_now_add=True)
    time_last_edited = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sub Categories"

    def __str__(self):
        return f"{self.name} {self.categories}"


class Project(models.Model):
    name = models.CharField(unique=True, max_length=20)
    short_description = models.CharField(max_length=255)
    long_description = models.TextField(null=True, blank=True)
    sub_categories = models.ManyToManyField(SubCategory)
    image = models.ImageField(null=True, blank=True)
    slug = models.SlugField()
    weight = models.IntegerField(
        default=0, help_text="level of importance")  # level of importance
    #
    repository_url = models.URLField(
        null=True, blank=True, help_text="url to code")
    repository_url_is_public = models.BooleanField(default=True)
    live_url = models.URLField(
        null=True, blank=True, help_text="url to live project")
    live_url_is_public = models.BooleanField(default=True)
    #
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_public = models.BooleanField(default=True)  # should it be shown?
    #
    time_added = models.DateTimeField(auto_now_add=True)
    time_last_edited = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['weight', '-start_date']

    def clean(self):
        if self.end_date is not None and self.start_date is not None and (self.start_date > self.end_date):
            raise ValidationError("End date cannot be before start date!")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.short_description}"
