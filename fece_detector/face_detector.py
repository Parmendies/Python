# face_recognition ve opencv kütüphanelerini import ederek başlıyoruz
import face_recognition  # type: ignore
import cv2


# opencv metodu olan VideoCapture ile webcam'den görüntü almayı başlatıyoruz // 0 default webcam video_capture = cv2.VideoCapture(0)
# Yukarıdaki "mennan sevim" resmini yüklüyoruz ve encoding bilgisini alıyoruz
bimo = face_recognition.load_image_file(
    '/home/bimo/Python/fece_detector/face_db/bimo/20240427_175110.jpg')
bimo_encoded = face_recognition.face_encodings(bimo)[0]

# Yukarıdaki "miray sevim" resmini yüklüyoruz ve encoding bilgisini alıyoruz
mal = face_recognition.load_image_file(
    "/home/bimo/Python/fece_detector/face_db/mal/Screenshot_20240427_172956_Gallery.jpg")
mal_encoded = face_recognition.face_encodings(mal)[0]


# Encoding ve açıklama kısmını burada tanımlıyoruz, birden fazla tanımlayabiliriz
known_face_encodings = [
    bimo_encoded,
    mal_encoded,
]
known_face_names = [
    "Bimo",
    "Mal"
]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
__nowPlaying = False

while True:
    # Videodan anlık bir kare yakalıyoruz
    ret, frame = video_capture.read()  # type: ignore

    # Aldığımız kareyi 1/4 oranında küçültüyoruz ve bu daha hızlı sonuç vermeyi sağlıyor
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # BGR(opencv) türündeki resmi RGB(face_recognition) formatına çeviriyoruz
    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
       # Uyumlu tüm yüzlerin lokasyonlarını bulan kodlar
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # Eşleşen yüzleri topla
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding)
            name = "Mal Değil"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                if name == "Bimo" and __nowPlaying == False:
                    print('hello')
                    globals()['__nowPlaying'] = True
                elif name == "Bilinmeyen":
                    print('stop')

            face_names.append(name)

    process_this_frame = not process_this_frame
    print(len(face_names))
    if len(face_names) == 0:
        print('stop')

    # Sonuçları göster
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Yüzü çerçeve içerisine al
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # "Mennan Sevim" etiketini oluştur
        cv2.rectangle(frame, (left, bottom - 35),
                      (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6),
                    font, 1.0, (255, 255, 255), 1)

    # Oluşan çerçeveyi ekrana yansıt
    cv2.imshow('Video', frame)

    # Çıkış için 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamerayı kapat
video_capture.release()  # type: ignore
cv2.destroyAllWindows()
