import cv2
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cascade_path = os.path.join(BASE_DIR, "server", "utils", "haarcascade_eye.xml")
output_path = os.path.join(BASE_DIR, "debug_iris", "live.png")

# Load Haar Cascade
eye_cascade = cv2.CascadeClassifier(cascade_path)
if eye_cascade.empty():
    print("❌ Haar cascade not found or failed to load.")
    exit(1)

# Ensure output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Start webcam
cap = cv2.VideoCapture(0)
print("📸 Show your eye to the webcam. Press 's' to capture, 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to capture frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in eyes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        break

    cv2.imshow("Live Iris Capture", frame)

    key = cv2.waitKey(1)
    if key == ord('s') and len(eyes) > 0:
        (x, y, w, h) = eyes[0]
        eye_region = gray[y:y+h, x:x+w]
        resized = cv2.resize(eye_region, (64, 64))
        cv2.imwrite(output_path, resized)
        print(f"✅ Cropped iris saved to: {output_path}")
        break
    elif key == ord('q'):
        print("❌ Quit without saving.")
        break

cap.release()
cv2.destroyAllWindows()
