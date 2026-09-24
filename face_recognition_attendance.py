import cv2
import face_recognition
import os
import csv
from datetime import datetime

# =========================
# 1. Known faces folder
# =========================

path = "known_faces"

known_face_encodings = []
known_face_names = []

# Load known face photos
for file in os.listdir(path):

    if file.lower().endswith((".jpg", ".jpeg", ".png")):

        image_path = os.path.join(path, file)

        image = face_recognition.load_image_file(image_path)

        encodings = face_recognition.face_encodings(image)

        if encodings:

            known_face_encodings.append(encodings[0])

            # Filename se person ka naam
            name = os.path.splitext(file)[0]

            known_face_names.append(name)


print("Known faces loaded:", known_face_names)


# =========================
# 2. Attendance file
# =========================

attendance_file = "attendance.csv"

if not os.path.exists(attendance_file):

    with open(
        attendance_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Name",
            "Date",
            "Time"
        ])


# =========================
# 3. Prevent duplicate attendance
# =========================

marked_today = set()


def mark_attendance(name):

    today = datetime.now().strftime("%Y-%m-%d")

    current_time = datetime.now().strftime("%H:%M:%S")


    # Same session mein dobara attendance nahi hogi
    if name.strip().lower() in marked_today:

        return


    # Existing attendance check karo
    with open(
        attendance_file,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.reader(file)

        # Header skip
        next(reader, None)

        for row in reader:

            if len(row) >= 2:

                existing_name = row[0].strip().lower()

                existing_date = row[1].strip()


                # Agar same person ki aaj attendance already hai
                if (
                    existing_name == name.strip().lower()
                    and existing_date == today
                ):

                    marked_today.add(
                        name.strip().lower()
                    )

                    return


    # New attendance save karo
    with open(
        attendance_file,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            name,
            today,
            current_time
        ])


    # Memory mein save karo
    marked_today.add(
        name.strip().lower()
    )


    print(
        "Attendance marked:",
        name,
        today,
        current_time
    )


# =========================
# 4. Start camera
# =========================

camera = cv2.VideoCapture(
    0,
    cv2.CAP_DSHOW
)

print("Camera started")


if not camera.isOpened():

    print("Camera open nahi ho raha.")

    exit()


# =========================
# 5. Face recognition loop
# =========================

while True:

    ret, frame = camera.read()


    if not ret:

        print("Camera frame nahi mil raha.")

        break


    # Faster processing ke liye resize
    small_frame = cv2.resize(
        frame,
        (0, 0),
        fx=0.25,
        fy=0.25
    )


    # BGR -> RGB
    rgb_small_frame = cv2.cvtColor(
        small_frame,
        cv2.COLOR_BGR2RGB
    )


    # Faces detect karo
    face_locations = face_recognition.face_locations(
        rgb_small_frame
    )


    face_encodings = face_recognition.face_encodings(
        rgb_small_frame,
        face_locations
    )


    # =========================
    # 6. Recognize faces
    # =========================

    for face_encoding, face_location in zip(
        face_encodings,
        face_locations
    ):

        matches = face_recognition.compare_faces(
            known_face_encodings,
            face_encoding,
            tolerance=0.5
        )


        name = "Unknown"


        if True in matches:

            index = matches.index(True)

            name = known_face_names[index]


            # Attendance mark karo
            mark_attendance(name)


        # Face coordinates
        top, right, bottom, left = face_location


        # Coordinates ko original size mein lao
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4


        # Face ke around box
        cv2.rectangle(
            frame,
            (left, top),
            (right, bottom),
            (0, 255, 0),
            2
        )


        # Naam show karo
        cv2.putText(
            frame,
            name,
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )


    # =========================
    # 7. Show camera
    # =========================

    cv2.imshow(
        "Face Recognition Attendance",
        frame
    )


    # Q press karke exit
    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# =========================
# 8. Close everything
# =========================

camera.release()

cv2.destroyAllWindows()

print("Camera closed.")