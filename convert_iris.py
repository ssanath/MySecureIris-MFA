import cv2
import os

# Ensure output directory exists
output_dir = os.path.join(os.getcwd(), "debug_iris")
os.makedirs(output_dir, exist_ok=True)

# ✅ Load Haar cascade using absolute path
cascade_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "server", "utils", "haarcascade_eye.xml"))
eye_cascade = cv2.CascadeClassifier(cascade_path)

# Start webcam
cap = cv2.VideoCapture(0)
print("📸 Starting webcam. Press 's' to capture, 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to capture frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in eyes:
        eye = gray[y:y+h, x:x+w]
        eye_resized = cv2.resize(eye, (64, 64))
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        break

    cv2.imshow("Register Iris - Press 's' to save", frame)

    key = cv2.waitKey(1)
    if key == ord('s') and 'eye_resized' in locals():
        path = os.path.join(output_dir, "registered.png")
        cv2.imwrite(path, eye_resized)
        print("✅ Registered iris saved to:", path)
        break
    elif key == ord('q'):
        print("❌ Quit without saving.")
        break

cap.release()
cv2.destroyAllWindows()
