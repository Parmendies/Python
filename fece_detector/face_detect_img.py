import cv2
import os
import numpy as np
from math import ceil

test_image = '/home/bimo/Python/fece_detector/Screenshot_20240427_175419_Gallery.jpg'
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()
min_confidence = 10
confidence = 0


def get_data():
    images = []
    image_label = []
    names = []
    cd = os.getcwd()
    dataset_dir = os.path.join(cd, 'face_db')
    folders = os.listdir(dataset_dir)
    for i in range(len(folders)):
        names.append(folders[i])
        wd = os.path.join(dataset_dir, folders[i])
        folder_imgs = os.listdir(wd)

        for j in folder_imgs:
            im = cv2.imread(os.path.join(wd, j), 0)
            faces = face_cascade.detectMultiScale(im, 1.1, 5, minSize=(50, 50))
            for (x, y, w, h) in faces:
                im_arr = np.array(im[x:x+w, y:y+h], 'uint8')
                if im_arr.size != 0:  # bazen boş veriyor!
                    images.append(im_arr)
                    image_label.append(i)

    cv2.destroyAllWindows()
    return images, image_label, names


# eğit
image_data, labels, names = get_data()
print(labels)
print(np.array(labels))

recognizer.train(image_data, np.array(labels))

# yuzleri bul
img = cv2.imread(test_image)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(
    gray, 1.1, 5, minSize=(100, 100))

for (x, y, w, h) in faces:  # yuzleri isaretle
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    test = gray[x:x+w, y:y+h]
    test_img = np.array(test, 'uint8')
    if (test_img.any()):  # img icinde yuz varsa tahmin et
        index, confidence = recognizer.predict(test_img)
    if (confidence >= min_confidence):  # tahmini yaz
        cv2.putText(img, names[index], (x, y+h+20),
                    cv2.FONT_HERSHEY_DUPLEX, .5, (0, 255, 0))
        cv2.putText(img, str(ceil(confidence))+"%", (x, y-20),
                    cv2.FONT_HERSHEY_DUPLEX, .5, (0, 255, 0))


cv2.imshow('img', img)  # ekrana bas
cv2.imwrite("output_detected.jpg", img)  # kaydet
cv2.destroyAllWindows()
