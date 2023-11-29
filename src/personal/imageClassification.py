from roboflow import Roboflow
from pathlib import Path
from django.conf import settings

rf = Roboflow(api_key="QggEFMO1t9ORFmzcnp7Y")
project = rf.workspace().project("classificationfridge")
model = project.version(1).model

# infer on a local image
def getImageInfo(image):
    classNames = set()
    imageLoc = Path(settings.MEDIA_ROOT, image)
    predictions = model.predict(str(imageLoc), confidence=40, overlap=30).json()['predictions']
    for prediction in predictions:
        classNames.add(prediction["class"])
    return classNames

# visualize your prediction
# model.predict("your_image.jpg", confidence=40, overlap=30).save("prediction.jpg")

# infer on an image hosted elsewhere
# print(model.predict("URL_OF_YOUR_IMAGE", hosted=True, confidence=40, overlap=30).json())