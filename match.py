import cv2
import os
import numpy as np

# Get absolute paths for both iris images
project_root = os.path.dirname(os.path.abspath(__file__))
registered_path = os.path.join(project_root, "debug_iris", "registered.png")
live_path = os.path.join(project_root, "debug_iris", "live.png")

def load_grayscale_image(path):
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return None
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"❌ Could not load image: {path}")
        return None
    return cv2.resize(img, (64, 64))

# Load images
registered = load_grayscale_image(registered_path)
live = load_grayscale_image(live_path)

if registered is None or live is None:
    print("❌ Iris images not found or invalid format.")
    exit(1)

# Compute mean absolute pixel difference
diff = np.abs(registered.astype(np.int32) - live.astype(np.int32))
score = np.mean(diff)

print(f"🔎 Similarity Score: {int(score)}")

# Matching threshold (adjust based on real test data)
THRESHOLD = 20  # lower = stricter match

if score < THRESHOLD:
    print("✅ Iris Match Found!")
    exit(0)
else:
    print("❌ Iris does not match.")
    exit(1)
