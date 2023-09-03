train.py

# training model
import cv2  # open cv library
import numpy as np  # for mathematical calculation
from os import listdir  # class of os module // when fetching data
from os.path import isfile, join

data_path = "C:/Users/sreev/Downloads/Project-2/LockSystem-main/LockSystem-main/Sample/"
onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]

Training_Data, Labels = [], []

for i, files in enumerate(onlyfiles):
    image_path = data_path + onlyfiles[i]
    images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    Training_Data.append(np.asarray(images, dtype=np.uint8))
    Labels.append(i)
Labels = np.asarray(Labels, dtype=np.int32)

model = cv2.face.LBPHFaceRecognizer_create()
model.train(np.asarray(Training_Data), np.asarray(Labels))
print("Congratulations model is TRAINED ... *_*...")
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
