from django.db import models

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    patient_id = models.CharField(max_length=100, null=False)
    patient_name = models.CharField(max_length=100, null=False)
    patient_sex = models.CharField(max_length=10, null=False)
    referring_physicians_name = models.CharField(max_length=100, null=False)
    requested_procedure_description = models.CharField(max_length=100, null = False)
    study_instance_uid = models.CharField(max_length=100, null=False)
    patient_birth_date = models.DateTimeField(null=False)
    station_id = models.IntegerField(null=False)

    def __str__(self):
        return f"Orders for {self.patient_name}"

class Modality(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

def __str__(self):
    return self.name
