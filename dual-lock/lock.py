import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
from datetime import date
import speech_recognition as sr
import winsound
import pyttsx3
import datetime
import smtplib
import math
import random

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

k = pyttsx3.init()
sound = k.getProperty('voices')
k.setProperty('voice', sound[0].id)
k.setProperty('rate', 130)
k.setProperty('pitch', 200)
count = 0

account_sid = "AC638bcb9ffa2623b79e6957e008234832"
auth_token = "01b809fa2706ab869e0b902312e49bbd"
twilio_number = "+12542724462"

client = Client(account_sid , auth_token)


def speak(text):
    k.say(text)
    k.runAndWait()

data_path = "C:/Users/sreev/Downloads/Project-2/LockSystem-main/LockSystem-main/Sample/"
onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]

Training_Data, Labels = [], []
name = ""
num = ""

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


def face_detector(img, size=0.5):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        i = 0
        if faces is ():
            return img, []

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
            roi = img[y:y + h, x:x + w]
            roi = cv2.resize(roi, (200, 200))
            i = i + 1

            if (i > 1):
                speak("multiple people detected")
                speak("Cannot proceed further")
                cap.release()
                cv2.destroyAllWindows()

        return img, roi


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if count < 1:
        image, face = face_detector(frame)
    img_copy = image.copy()
    cv2.imshow("Face Cropper", image)
    try:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        result = model.predict(face)
        name = onlyfiles[result[0]].split("_")[0]
        num = onlyfiles[result[0]].split("_")[1]
        print(num)
        if result[1] < 500:
            Confidence = int(100 * (1 - (result[1]) / 300))

        if 75 < Confidence:
            Date = date.today()
            time = datetime.datetime.now().strftime('%I:%M %p')
            cv2.destroyWindow('Face not found')
            cv2.putText(image, "HELLO "+name.upper(), (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            speak(name+" is found at  " + time)


            cv2.imshow("Face Cropper", image)
            count = 1

            listener = sr.Recognizer()
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0].id)
            cap.release()
            cv2.destroyAllWindows()
        else:
            pass

        if count == 1:
            def talk(text):
                engine.say(text)
                engine.runAndWait()


            def take_command():
                try:
                    mic = sr.Microphone(device_index=2)
                    print(mic.list_working_microphones())
                    with mic as source:
                        print(sr.Microphone.list_microphone_names())
                        talk("Hello "+name+" Say lock ")
                        print("listening...")
                        voice = listener.listen(source)
        command = listener.recognize_google(voice)
                        command = command.lower()
                        print(command)
                        if 'doodle' in command:
                            command = command.replace('doodle', '')
                            speak(command)
                except:
                    pass
                return command

            command = take_command()

            if 'lock' in command:
                digits = "0123456789"
                OTP = ""
                List = []
                for i in range(0, 4):
                    OTP += digits[math.floor(random.random() * 10)]
                for i in OTP:
                    List.append(i)
                otp = OTP + " is your OTP"
                try:
                    message = client.messages.create(
                        from_="+12542724462",
                        body=f'Your OTP is {otp}',
                        to='+91' + num,
                    )
                except TwilioRestException:
                    print('Max OTP send limit reached... Try again after 10 minutes!')
                print(message)
                a = input("Enter Your OTP >>: ")
                if a == OTP:
                    print("Verified")
                else:
                    print("Please Check your OTP again")

            else:
                talk("Please say the command again")

        else:
            winsound.Beep(1000, 200)
            cv2.putText(image, "CAN'T RECOGNISE", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow("Face Cropper", image)
            print(Confidence)
            print("Unauthorise user")
            cap.release()
            cv2.destroyAllWindows()
            talk("Multiple People Detected")
            talk("Only one person at a time")

    except:
        # speak("face not found")
        if count ==0:
            cv2.putText(img_copy, "Face not FoUnD", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

            cv2.imshow("Face not found", img_copy)
            pass
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break

# cap.release()
# cv2.destroyAllWindows()
