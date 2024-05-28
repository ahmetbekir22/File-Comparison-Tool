from django.shortcuts import render
from .forms import ImageUploadForm
import easyocr
import cv2
import numpy as np


def scan_image_upload_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data['image']
            image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

            # EasyOCR okuyucusunu başlatın
            reader = easyocr.Reader(['en'])  # 'en' yerine başka diller de ekleyebilirsiniz

            # Görüntüyü gri tonlamaya çevirin
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # OCR işlemi yapın
            results = reader.readtext(gray)

            # Tanınan metinleri ve koordinatları saklayın
            recognized_text = []
            for (bbox, text, prob) in results:
                recognized_text.append({
                    'text': text,
                    'probability': prob,
                    'bbox': bbox
                })
                # Metin kutusunu görüntü üzerinde çizin
                (top_left, top_right, bottom_right, bottom_left) = bbox
                top_left = tuple(map(int, top_left))
                bottom_right = tuple(map(int, bottom_right))
                cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
                cv2.putText(image, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # Görüntüyü kaydedin ve görüntü dosyasını context'e ekleyin
            result_image_path = 'media/result_image.jpg'
            cv2.imwrite(result_image_path, image)

            return render(request, 'scan_image_result.html', {
                'recognized_text': recognized_text,
                'result_image_path': result_image_path
            })
    else:
        form = ImageUploadForm()
    return render(request, 'scan_image_upload.html', {'form': form})
