import cv2
# Face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
# Camera start
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not camera.isOpened():
    print("Camera open nahi ho raha.")
    exit()
print("Face detection start ho gaya!")
while True:
    ret, frame = camera.read()
    if not ret:
        print("Video frame nahi mil raha.")
        break
    # Image ko grayscale mein convert karo
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Face detect karo
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    # Face ke around box banao
    for (x, y, w, h) in faces:
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )
    # Camera screen dikhao
    cv2.imshow("Face Detection", frame)
    # Q press karke close
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
camera.release()
cv2.destroyAllWindows()