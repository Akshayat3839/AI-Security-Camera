import cv2
import time

# Open camera
cap = cv2.VideoCapture(0)

# Read first two frames
ret, frame1 = cap.read()
ret, frame2 = cap.read()

motion_detected = False

while cap.isOpened():

    # Find difference between frames
    diff = cv2.absdiff(frame1, frame2)

    # Convert to grayscale
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Blur to remove noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold to get motion areas
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # Dilate to fill gaps
    dilated = cv2.dilate(thresh, None, iterations=3)

    # Find contours (motion areas)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False

    for contour in contours:
        if cv2.contourArea(contour) < 1500:
            continue

        motion_detected = True

        # Draw rectangle around motion
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Show status text
    if motion_detected:
        cv2.putText(frame1, "MOTION DETECTED!", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    else:
        cv2.putText(frame1, "No Motion", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display output
    cv2.imshow("AI Security Camera - Motion Detection", frame1)

    # Update frames
    frame1 = frame2
    ret, frame2 = cap.read()

    # Exit key
    if cv2.waitKey(10) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
