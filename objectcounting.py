import cv2

# Initialize the webcam
cap = cv2.VideoCapture(0)  # Default webcam index, try 1 or 2 if not working

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not access the camera.")
    exit()

# Load a pre-trained object detection model (Haar Cascade for face detection)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    # Capture each frame from the webcam
    ret, frame = cap.read()

    # If frame was not captured, break the loop
    if not ret:
        print("Error: Failed to capture image.")
        break

    # Convert the image to grayscale (required for detection)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Draw bounding boxes around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Count the number of detected faces
    face_count = len(faces)

    # Display the face count on the image
    cv2.putText(frame, f"Faces: {face_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame with the bounding boxes and face count
    cv2.imshow("Object Detection - Press 'q' to quit", frame)

    # If 'q' is pressed, exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()
