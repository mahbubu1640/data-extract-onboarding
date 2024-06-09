from django.contrib.auth.models import User
from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class DocumentSet(models.Model):
    name = models.CharField(max_length=100)
    countries = models.ManyToManyField(Country)
    has_backside = models.BooleanField(default=False)
    ocr_labels = models.TextField()

    def __str__(self):
        return self.name

class Customer(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    surname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_customers')

    def __str__(self):
        return f"{self.firstname} {self.surname}"

class CustomerDocument(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    attached_file = models.FileField(upload_to='documents/')
    extracted_json = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.customer.firstname} {self.customer.surname}"
