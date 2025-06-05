import cv2
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print("✅ Webcam opened successfully.")
else:
    print("❌ Webcam failed to open.")
cap.release()
