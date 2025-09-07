from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from ultralytics import YOLO
from io import BytesIO
from PIL import Image
import base64

model = YOLO("yolov8n.pt")  # or your trained model

def homepage(request):
    return HttpResponse("<h1>Welcome to Tree ID</h1><p><a href='/streetview/'>Go to Street View Scanner</a></p>")

def streetview(request):
    return render(request, "streetview.html")

@csrf_exempt
def streetview_scan(request):
    context = {}
    if request.method == "POST":
        img_data = request.POST.get("image")
        if img_data:
            img_data = img_data.replace("data:image/jpeg;base64,", "")
            image = Image.open(BytesIO(base64.b64decode(img_data)))
            raw_path = "media/captured_streetview.jpg"
            image.save(raw_path)

            results = model(raw_path)
            predict_path = "media/predicted_streetview.jpg"
            results[0].save(filename=predict_path)

            probs = results[0].probs
            label = results[0].names[probs.top1] if probs else "No detection"

            context = {
                "original": "/" + raw_path,
                "result": "/" + predict_path,
                "label": label
            }

    return render(request, "streetview_result.html", context)
