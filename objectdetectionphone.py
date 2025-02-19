import cv2
import numpy as np

# Load YOLO model
try:
    net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
except Exception as e:
    print(f"Error loading YOLO model: {e}")
    exit()

# Load COCO class labels
try:
    with open('coco.names', 'r') as f:
        classes = f.read().strip().split('\n')
except Exception as e:
    print(f"Error loading class names: {e}")
    exit()

# Connect to phone camera (DroidCam)
camera_url = "http://192.168.136.96:4747/video"  # Change if necessary
cap = cv2.VideoCapture("http://192.168.136.96:4747/video", cv2.CAP_FFMPEG)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Lower resolution
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  
cap.set(cv2.CAP_PROP_FPS, 30)  # Try forcing 30 FPS



if not cap.isOpened():
    print("Error: Unable to connect to the camera. Check the IP and port.")
    exit()

# Get output layer names
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

while True:
    # Capture frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read frame. Check the camera connection.")
        break

    # Resize frame for faster processing
    frame = cv2.resize(frame, (320, 240))  # Lower resolution
    height, width = frame.shape[:2]

    # Create a blob
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Perform forward pass
    detections = net.forward(output_layers)

    boxes, confidences, class_ids = [], [], []

    # Process detections
    for output in detections:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:  # Confidence threshold
                box = detection[0:4] * np.array([width, height, width, height])
                (centerX, centerY, w, h) = box.astype('int')

                x = int(centerX - (w / 2))
                y = int(centerY - (h / 2))

                boxes.append([x, y, int(w), int(h)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply Non-Maxima Suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Draw bounding boxes
    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            label = f"{classes[class_ids[i]]} {confidences[i]:.2f}"
            color = (0, 255, 0)  # Green color for bounding box

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Display frame
    cv2.imshow('Real-Time Object Detection', frame)

    # Exit loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
