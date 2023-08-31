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


class Patient(models.Model):
    PatientNo = models.CharField(max_length=50, null= True, blank=True)
    PatientName = models.TextField(max_length=225, null= True, blank=True)
    PatientID = models.CharField(max_length=50, null= True, blank=True)
    PatientBirthDate = models.DateTimeField(auto_now=True)
    PatientSex = models.CharField(max_length=50, null= True, blank=True)


# Create your models here.
class Study(models.Model):
    study_no = models.CharField(max_length=50, null=True,blank=True)
    PatientNo = models.ForeignKey(Patient,on_delete=models.CASCADE, null=True,blank=True)
    study_instance_uid = models.CharField(max_length=50, null=True,blank=True)
    accession_no = models.CharField(max_length=50, null=True,blank=True)
    study_description = models.TextField(max_length=255,null=True,blank=True)
    study_datetime = models.DateTimeField(auto_now=True)

class Series(models.Model):
    series_no = models.CharField(max_length=50, null=True,blank=True)
    study_no = models.ForeignKey(Study,on_delete=models.CASCADE, null=True,blank=True)
    series_instance_uid = models.CharField(max_length=50, null=True,blank=True)
    series_number = models.CharField(max_length=50, null=True,blank=True)
    accession_no = models.CharField(max_length=50, null=True,blank=True)
    series_description = models.TextField(max_length=255,null=True,blank=True)
    series_datetime = models.DateTimeField(auto_now=True,)

class Image(models.Model):
    sop_instance_uid = models.CharField(max_length=50, blank=True, null=True)
    image = models.FileField(max_length=255, blank=True, null=True)
    modality = models.CharField(max_length=15, blank=True, null=True)
    instance_number = models.CharField(max_length=50, blank=True, null=True)
    content_datetime = models.DateTimeField()
    patient_orientation = models.CharField(max_length=50, blank=True, null=True)
    samples_per_pixel = models.PositiveIntegerField(null = True, blank= True)
    photometric_interpretation = models.CharField(max_length=50, blank=True, null=True)
    rows = models.PositiveIntegerField(null=True,blank=True)
    columns = models.PositiveIntegerField(null=True,blank=True)
    bits_allocated = models.PositiveIntegerField(null=True,blank=True)
    bits_stored = models.PositiveIntegerField(null=True,blank=True)
    high_bit = models.PositiveIntegerField(null=True,blank=True)
    pixel_representation = models.PositiveIntegerField(null=True, blank= True)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, blank=True, null=True)

class File(models.Model):
    file_no = models.CharField(max_length=50,null=True, blank= True)
    imageno = models.ForeignKey(Image,on_delete=models.CASCADE, null=True, blank= True)
    file_data = models.CharField(max_length=50, null=True, blank= True)
    file_name = models.CharField(max_length=50, null=True, blank= True)
    file_size = models.CharField(max_length=50, null=True, blank= True)
    report_no = models.CharField(max_length=50, null=True, blank= True)

class Report(models.Model):
    reportno = models.ForeignKey(File,on_delete=models.CASCADE, null=True, blank= True)
    report_data = models.CharField(max_length=50, null=True, blank= True)
    report_size = models.CharField(max_length=50, null=True, blank= True)

class ModalitySystem(models.Model):
    study = models.ForeignKey(Study,on_delete=models.CASCADE,null=True,blank=True)
    series = models.ForeignKey(Series,on_delete=models.CASCADE,null=True,blank=True)
    image = models.ForeignKey(Image,on_delete=models.CASCADE,null=True,blank=True)
    file = models.ForeignKey(File,on_delete=models.CASCADE,null=True,blank=True)
    report = models.ForeignKey(Report,on_delete=models.CASCADE,null=True,blank=True)