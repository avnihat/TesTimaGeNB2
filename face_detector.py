from pathlib import Path
import cv2

def detect_faces(image_path, cascade_path=None):
    img_path = str(image_path)
    try:
        img = cv2.imread(img_path)
        if img is None:
            return {'face_count': 0, 'note': 'Görüntü açılamadı'}
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if cascade_path is None:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
        if face_cascade.empty():
            return {'face_count': 0, 'note': 'Cascade bulunamadı'}
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        return {'face_count': int(len(faces))}
    except Exception as e:
        return {'face_count': 0, 'note': str(e)}
