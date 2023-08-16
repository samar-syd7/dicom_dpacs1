from django.conf import settings
from pydicom import dcmread

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import pydicom
from PIL import Image
import io
import os
import numpy as np
import cv2
import pydicom

def upload_convert_store(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        fs = FileSystemStorage(location="media/")
        filename= fs.save(image.name, image)
        # dicom_image = DicomImage(image=filename)
        


        ds = dcmread(f"media/{filename}")
        pixel_array_numpy = ds.pixel_array
        dicom_path = os.path.join("media/", filename)
        image = dicom_path.replace('.DCM', '.jpg')
        print(image)
        cv2.imwrite(os.path.join(image), pixel_array_numpy)

        jpg_filename = image.replace('media/','')

        instance_uid = "1.2.3.4.5.6"
        ds.SOPInstanceUID = instance_uid
        ds.PixelData = image.read()

        return render(request, 'upload_convert_store.html')
    
    return render(request, 'upload_convert_store.html')
    