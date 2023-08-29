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

# class Modality(models.Model):
#     name = models.CharField(max_length=100, null=False)
#     description = models.TextField(null=False)
#     created_at = models.DateTimeField(auto_now_add=True, null=False)
#     updated_at = models.DateTimeField(auto_now=True, null=False)

# class Study(models.Model):
#     study_instance_uid = models.CharField(max_length=100, unique=True)
#     patient_name = models.CharField(max_length=100)
#     patient_id = models.CharField(max_length=20)
    

# class Series(models.Model):
#     series_instance_uid = models.CharField(max_length=100, unique=True)
#     study = models.ForeignKey(Study, on_delete=models.CASCADE)
    

# class Image(models.Model):
#     series = models.ForeignKey(Series, on_delete=models.CASCADE)
#     dicom_path = models.FilePathField()

class Patient(models.Model):
    PatientNo = models.CharField(max_length=50, null= True, blank=True)
    PatientName = models.TextField(max_length=225, null= True, blank=True)
    PatientID = models.CharField(max_length=50, null= True, blank=True)
    PatientBirthDate = models.DateTimeField(auto_now=True)
    PatientSex = models.CharField(max_length=50, null= True, blank=True)


# Create your models here.
class Study(models.Model):
    study_no = models.CharField(max_length=50,null=True,blank=True)
    PatientNo = models.ForeignKey(Patient,on_delete=models.CASCADE, null=True)
    study_instance_uid = models.CharField(max_length=50, null=True,blank=True)
    accession_no = models.CharField(max_length=50, null=True,blank=True)
    study_descripton = models.TextField(max_length=255,null=True,blank=True)
    study_datetime = models.DateTimeField(auto_now=True)

class Series(models.Model):
    series_no = models.CharField(max_length=50,null=True,blank=True)
    study_no = models.ForeignKey(Study,on_delete=models.CASCADE, null=True,blank=True)
    series_instance_uid = models.CharField(max_length=50, null=True,blank=True)
    series_number = models.CharField(max_length=50 ,null=True,blank=True)
    accession_no = models.CharField(max_length=50, null=True,blank=True)
    series_description = models.TextField(max_length=255,null=True,blank=True)
    series_datetime = models.DateTimeField(auto_now=True,)

class Image(models.Model):
    image = models.FileField(null=True,blank=True)
    image_no = models.CharField(max_length=50, null=True,blank=True)
    series = models.ForeignKey(Series,on_delete=models.CASCADE, null=True,blank=True)
    sop_instance_uid = models.CharField(max_length=50, null=True,blank=True)
    modality = models.CharField(max_length=15, null=True,blank=True)
    bodypart_examined = models.CharField(max_length=50, null=True,blank=True)
    instance_number = models.CharField(max_length=50, null=True,blank=True)
    content_datetime = models.DateTimeField(auto_now=True)
    numberofwaveformchannel = models.CharField(max_length=50, null=True,blank=True)
    numberofwaveformsamples = models.CharField(max_length=50, null=True,blank=True)
    sampling_frequency = models.CharField(max_length=50, null=True,blank=True)
    waveformbitsallocated = models.CharField(max_length=50, null=True,blank=True)

class File(models.Model):
    file_no = models.CharField(max_length=50, null=True,blank=True)
    imageno = models.ForeignKey(Image,on_delete=models.CASCADE, null=True,blank=True)
    file_data = models.CharField(max_length=50, null=True,blank=True)
    file_name = models.CharField(max_length=50, null=True,blank=True)
    file_size = models.CharField(max_length=50, null=True,blank=True)
    report_no = models.CharField(max_length=50, null=True,blank=True)

class Report(models.Model):
    reportno = models.ForeignKey(File,on_delete=models.CASCADE, null=True,blank=True)
    report_data = models.CharField(max_length=50, null=True,blank=True)
    report_size = models.CharField(max_length=50, null=True,blank=True)

class ModalitySystem(models.Model):
    study = models.ForeignKey(Study,on_delete=models.CASCADE,null=True,blank=True)
    series = models.ForeignKey(Series,on_delete=models.CASCADE,null=True,blank=True)
    image = models.ForeignKey(Image,on_delete=models.CASCADE,null=True,blank=True)
    file = models.ForeignKey(File,on_delete=models.CASCADE,null=True,blank=True)
    report = models.ForeignKey(Report,on_delete=models.CASCADE,null=True,blank=True)

def __str__(self):
    return self.name
