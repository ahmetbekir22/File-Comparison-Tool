from django.shortcuts import render
from .forms import ImageUploadForm
from .image_comparison import structural_sim  # Import the function from image_comparison.py
from skimage.transform import resize
import cv2
import numpy as np
import base64

def image_upload_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img1 = form.cleaned_data['image1']
            img2 = form.cleaned_data['image2']

            img1 = cv2.imdecode(np.frombuffer(img1.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
            img2 = cv2.imdecode(np.frombuffer(img2.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

            img2_resized = resize(img2, (img1.shape[0], img1.shape[1]), anti_aliasing=True, preserve_range=True)
            ssim = structural_sim(img1, img2_resized) * 100  # Convert to percentage

            # Convert images to base64 for displaying in HTML
            _, buffer1 = cv2.imencode('.png', img1)
            img1_base64 = base64.b64encode(buffer1).decode('utf-8')
            _, buffer2 = cv2.imencode('.png', img2)
            img2_base64 = base64.b64encode(buffer2).decode('utf-8')

            return render(request, 'image_compare.html', {
                'ssim': ssim,
                'img1_base64': img1_base64,
                'img2_base64': img2_base64
            })
    else:
        form = ImageUploadForm()
    return render(request, 'image_upload.html', {'form': form})