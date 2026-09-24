import cv2
print("1. Program start")
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
print("2. Camera opened:", camera.isOpened())
ret, frame = camera.read()
print("3. Frame mila:", ret)
if ret:
    print("4. Video frame successfully mil gaya")
    cv2.imshow("Camera Test", frame)
    cv2.waitKey(5000)
camera.release()
cv2.destroyAllWindows()
print("5. Program complete")