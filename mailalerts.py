import cv2
import numpy as np
import time
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send an email
def send_email(subject, body, to_email):
    from_email = "mfouzhan@gmail.com"
    password = "etfa swci kzmd jcaf"
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, password)
        
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server.sendmail(from_email, to_email, msg.as_string())

# Load YOLO model with CUDA optimization
net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

with open('coco.names', 'r') as f:
    classes = f.read().strip().split('\n')

cap = cv2.VideoCapture(0)
frame = None

def read_frames():
    global frame
    while cap.isOpened():
        ret, temp_frame = cap.read()
        if ret:
            frame = temp_frame

threading.Thread(target=read_frames, daemon=True).start()

animal_classes = ['dog', 'cat', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe']
to_email = "aswinkumar5306@gmail.com "

# Store animals already alerted to avoid duplicate emails
alerted_animals = set()

while True:
    if frame is None:
        continue
    
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    output_layers = [net.getLayerNames()[i - 1] for i in net.getUnconnectedOutLayers().flatten()]
    detections = net.forward(output_layers)
    
    boxes = []
    confidences = []
    class_ids = []

    for output in detections:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.4:
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                w = int(detection[2] * frame.shape[1])
                h = int(detection[3] * frame.shape[0])

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.3)

    if len(indexes) > 0:
        for i in indexes.flatten() if isinstance(indexes, np.ndarray) else indexes[0]:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]

            color = (0, 255, 0) if label in animal_classes else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Send alert for newly detected animals only
            if label in animal_classes and label not in alerted_animals:
                send_email("🚨 Animal Detection Alert!", f"⚠️ A wild {label} has been detected on your premises. Stay cautious!", to_email)
                alerted_animals.add(label)
                print(f"Alert sent for: {label}")

    cv2.imshow('Real-Time Object Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
