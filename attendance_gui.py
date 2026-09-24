import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog, ttk
import subprocess
import sys
import os
import shutil
import csv
from datetime import datetime
from openpyxl import Workbook


# =========================================================
# COLORS
# =========================================================

BG_COLOR = "#f4f6f8"
CARD_COLOR = "#ffffff"
TEXT_COLOR = "#1f2937"
BUTTON_COLOR = "#2563eb"
BUTTON_HOVER = "#1d4ed8"
DANGER_COLOR = "#dc2626"
GREEN_COLOR = "#16a34a"
ORANGE_COLOR = "#ea580c"

# Admin login details
ADMIN_USERNAME = "admin"

# Admin password
# The login password is fixed to 1234.
ADMIN_PASSWORD = "1234"

# =========================================================
# MAIN WINDOW
# =========================================================

window = tk.Tk()

window.title(
    "Face Recognition Attendance System"
)

window.geometry(
    "750x780"
)

window.configure(
    bg=BG_COLOR
)

window.resizable(
    False,
    False
)

# Main window hidden until login
window.withdraw()


# =========================================================
# START ATTENDANCE
# =========================================================

def start_attendance():

    try:

        subprocess.run(
            [sys.executable, "face_recognition_attendance.py"]
        )

        update_student_count()
        update_attendance_summary()

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# =========================================================
# ADD STUDENT
# =========================================================

def add_student():

    name = name_entry.get().strip()

    if not name:

        messagebox.showwarning(
            "Name Required",
            "Please enter student name."
        )

        return

    photo_path = filedialog.askopenfilename(
        title="Select Student Photo",
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png")
        ]
    )

    if not photo_path:
        return

    os.makedirs(
        "known_faces",
        exist_ok=True
    )

    extension = os.path.splitext(
        photo_path
    )[1]

    destination = os.path.join(
        "known_faces",
        name + extension
    )

    # Duplicate student check
    for file in os.listdir("known_faces"):

        existing_name = os.path.splitext(file)[0]

        if existing_name.lower() == name.lower():

            messagebox.showwarning(
                "Student Already Exists",
                f"{name} is already registered."
            )

            return

    try:

        shutil.copy2(
            photo_path,
            destination
        )

        messagebox.showinfo(
            "Student Added",
            f"{name} successfully added!"
        )

        name_entry.delete(
            0,
            tk.END
        )

        update_student_count()

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"Unable to add student.\n\n{e}"
        )


# =========================================================
# UPDATE STUDENT COUNT
# =========================================================

def update_student_count():

    count = 0

    if os.path.exists("known_faces"):

        for file in os.listdir("known_faces"):

            if file.lower().endswith(
                (".jpg", ".jpeg", ".png")
            ):

                count += 1

    count_label.config(
        text=str(count)
    )


# =========================================================
# UPDATE ATTENDANCE SUMMARY
# =========================================================

def update_attendance_summary():

    total_records = 0
    today_attendance = 0

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    if os.path.exists("attendance.csv"):

        try:

            with open(
                "attendance.csv",
                "r",
                newline="",
                encoding="utf-8"
            ) as file:

                reader = csv.reader(file)

                next(
                    reader,
                    None
                )

                for row in reader:

                    if len(row) >= 3:

                        total_records += 1

                        if row[1].strip() == today:

                            today_attendance += 1

        except Exception:

            pass

    total_records_label.config(
        text=str(total_records)
    )

    today_label.config(
        text=str(today_attendance)
    )


# =========================================================
# DASHBOARD
# =========================================================

def dashboard():

    dashboard_window = tk.Toplevel(window)

    dashboard_window.title(
        "Attendance Dashboard"
    )

    dashboard_window.geometry(
        "800x650"
    )

    dashboard_window.configure(
        bg=BG_COLOR
    )

    dashboard_window.resizable(
        False,
        False
    )


    tk.Label(
        dashboard_window,
        text="Attendance Dashboard",
        font=("Segoe UI", 24, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        pady=(25, 5)
    )


    tk.Label(
        dashboard_window,
        text=datetime.now().strftime("%d %B %Y"),
        font=("Segoe UI", 11),
        bg=BG_COLOR,
        fg="#6b7280"
    ).pack(
        pady=(0, 20)
    )


    # Read data

    total_students = 0
    total_attendance = 0
    today_attendance = 0

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )


    # Count students

    if os.path.exists("known_faces"):

        for file in os.listdir("known_faces"):

            if file.lower().endswith(
                (".jpg", ".jpeg", ".png")
            ):

                total_students += 1


    # Count attendance

    if os.path.exists("attendance.csv"):

        try:

            with open(
                "attendance.csv",
                "r",
                newline="",
                encoding="utf-8"
            ) as file:

                reader = csv.reader(file)

                next(reader, None)

                for row in reader:

                    if len(row) >= 3:

                        total_attendance += 1

                        if row[1].strip() == today:

                            today_attendance += 1

        except Exception:

            pass


    # Percentage

    if total_students > 0:

        percentage = (
            today_attendance /
            total_students
        ) * 100

    else:

        percentage = 0


    # CARDS

    cards_frame = tk.Frame(
        dashboard_window,
        bg=BG_COLOR
    )

    cards_frame.pack(
        pady=10
    )


    def create_card(
        parent,
        title,
        value,
        row,
        column
    ):

        card = tk.Frame(
            parent,
            bg=CARD_COLOR,
            width=330,
            height=120,
            bd=1,
            relief="solid"
        )

        card.grid(
            row=row,
            column=column,
            padx=10,
            pady=10
        )

        card.grid_propagate(
            False
        )


        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 11),
            bg=CARD_COLOR,
            fg="#6b7280"
        ).pack(
            pady=(18, 5)
        )


        tk.Label(
            card,
            text=value,
            font=("Segoe UI", 25, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack()


    create_card(
        cards_frame,
        "Registered Students",
        total_students,
        0,
        0
    )


    create_card(
        cards_frame,
        "Total Attendance Records",
        total_attendance,
        0,
        1
    )


    create_card(
        cards_frame,
        "Today's Attendance",
        today_attendance,
        1,
        0
    )


    create_card(
        cards_frame,
        "Today's Percentage",
        f"{percentage:.1f}%",
        1,
        1
    )


    # CHART

    def show_chart():

        import matplotlib.pyplot as plt

        present = today_attendance

        absent = max(
            total_students - today_attendance,
            0
        )

        labels = [
            "Present",
            "Absent"
        ]

        values = [
            present,
            absent
        ]

        plt.figure(
            figsize=(7, 5)
        )

        plt.bar(
            labels,
            values
        )

        plt.title(
            "Today's Attendance"
        )

        plt.xlabel(
            "Status"
        )

        plt.ylabel(
            "Number of Students"
        )

        plt.tight_layout()

        plt.show()


    tk.Button(
        dashboard_window,
        text="📊  Show Attendance Chart",
        font=("Segoe UI", 13, "bold"),
        width=28,
        height=2,
        bg=BUTTON_COLOR,
        fg="white",
        activebackground=BUTTON_HOVER,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=show_chart
    ).pack(
        pady=25
    )


# =========================================================
# EXPORT TO EXCEL
# =========================================================

def export_to_excel(
    attendance_data,
    parent_window
):

    if not attendance_data:

        messagebox.showwarning(
            "No Records",
            "There are no attendance records to export.",
            parent=parent_window
        )

        return


    save_path = filedialog.asksaveasfilename(
        parent=parent_window,
        title="Save Attendance Excel File",
        defaultextension=".xlsx",
        filetypes=[
            ("Excel Files", "*.xlsx")
        ],
        initialfile="attendance.xlsx"
    )


    if not save_path:

        return


    try:

        workbook = Workbook()

        sheet = workbook.active

        sheet.title = "Attendance"


        sheet.append([
            "Student Name",
            "Date",
            "Time"
        ])


        for record in attendance_data:

            sheet.append([
                record[0],
                record[1],
                record[2]
            ])


        sheet.column_dimensions["A"].width = 25
        sheet.column_dimensions["B"].width = 18
        sheet.column_dimensions["C"].width = 18


        workbook.save(
            save_path
        )


        messagebox.showinfo(
            "Export Successful",
            "Attendance successfully exported to Excel!\n\n"
            + save_path,
            parent=parent_window
        )


    except Exception as e:

        messagebox.showerror(
            "Export Error",
            str(e),
            parent=parent_window
        )


# =========================================================
# VIEW ATTENDANCE
# =========================================================

def view_attendance():

    if not os.path.exists("attendance.csv"):

        messagebox.showwarning(
            "No Attendance",
            "Attendance file not found."
        )

        return


    attendance_window = tk.Toplevel(
        window
    )

    attendance_window.title(
        "Attendance Records"
    )

    attendance_window.geometry(
        "900x650"
    )

    attendance_window.configure(
        bg=BG_COLOR
    )

    attendance_window.resizable(
        False,
        False
    )


    tk.Label(
        attendance_window,
        text="Attendance Records",
        font=("Segoe UI", 22, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        pady=15
    )


    # SEARCH

    search_frame = tk.Frame(
        attendance_window,
        bg=BG_COLOR
    )

    search_frame.pack(
        pady=8
    )


    tk.Label(
        search_frame,
        text="Student:",
        font=("Segoe UI", 11, "bold"),
        bg=BG_COLOR
    ).grid(
        row=0,
        column=0,
        padx=5
    )


    student_search = tk.Entry(
        search_frame,
        font=("Segoe UI", 11),
        width=20
    )

    student_search.grid(
        row=0,
        column=1,
        padx=5
    )


    tk.Label(
        search_frame,
        text="Date:",
        font=("Segoe UI", 11, "bold"),
        bg=BG_COLOR
    ).grid(
        row=0,
        column=2,
        padx=5
    )


    date_search = tk.Entry(
        search_frame,
        font=("Segoe UI", 11),
        width=15
    )

    date_search.grid(
        row=0,
        column=3,
        padx=5
    )


    # LOAD DATA

    attendance_data = []


    try:

        with open(
            "attendance.csv",
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.reader(file)

            next(reader, None)

            for row in reader:

                if len(row) >= 3:

                    attendance_data.append(
                        (
                            row[0],
                            row[1],
                            row[2]
                        )
                    )


    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )

        return


    # TABLE

    table_frame = tk.Frame(
        attendance_window,
        bg=BG_COLOR
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=10
    )


    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical"
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )


    table = ttk.Treeview(
        table_frame,
        columns=(
            "Name",
            "Date",
            "Time"
        ),
        show="headings",
        yscrollcommand=scrollbar.set,
        height=12
    )


    scrollbar.config(
        command=table.yview
    )


    table.heading(
        "Name",
        text="Student Name"
    )

    table.heading(
        "Date",
        text="Date"
    )

    table.heading(
        "Time",
        text="Time"
    )


    table.column(
        "Name",
        width=280,
        anchor="center"
    )

    table.column(
        "Date",
        width=220,
        anchor="center"
    )

    table.column(
        "Time",
        width=220,
        anchor="center"
    )


    table.pack(
        fill="both",
        expand=True
    )


    def display_records(records):

        for item in table.get_children():

            table.delete(item)


        for record in records:

            table.insert(
                "",
                "end",
                values=record
            )


    display_records(
        attendance_data
    )


    def get_current_records():

        student_text = (
            student_search
            .get()
            .strip()
            .lower()
        )

        date_text = (
            date_search
            .get()
            .strip()
            .lower()
        )


        filtered_records = []


        for record in attendance_data:

            student_match = (
                student_text == ""
                or student_text in record[0].lower()
            )


            date_match = (
                date_text == ""
                or date_text in record[1].lower()
            )


            if student_match and date_match:

                filtered_records.append(
                    record
                )


        return filtered_records


    def search_attendance(event=None):

        display_records(
            get_current_records()
        )


    student_search.bind(
        "<KeyRelease>",
        search_attendance
    )

    date_search.bind(
        "<KeyRelease>",
        search_attendance
    )


    # BUTTONS

    button_frame = tk.Frame(
        attendance_window,
        bg=BG_COLOR
    )

    button_frame.pack(
        pady=8
    )


    def clear_search():

        student_search.delete(
            0,
            tk.END
        )

        date_search.delete(
            0,
            tk.END
        )

        display_records(
            attendance_data
        )


    tk.Button(
        button_frame,
        text="Clear Search",
        font=("Segoe UI", 11, "bold"),
        width=15,
        command=clear_search
    ).grid(
        row=0,
        column=0,
        padx=10
    )


    tk.Button(
        button_frame,
        text="Export to Excel",
        font=("Segoe UI", 11, "bold"),
        width=18,
        command=lambda: export_to_excel(
            get_current_records(),
            attendance_window
        )
    ).grid(
        row=0,
        column=1,
        padx=10
    )


    tk.Label(
        attendance_window,
        text="Date format: YYYY-MM-DD",
        font=("Segoe UI", 9),
        bg=BG_COLOR,
        fg="#6b7280"
    ).pack(
        pady=3
    )


# =========================================================
# MANAGE STUDENTS
# =========================================================

def manage_students():

    manage_window = tk.Toplevel(
        window
    )

    manage_window.title(
        "Manage Students"
    )

    manage_window.geometry(
        "550x500"
    )

    manage_window.configure(
        bg=BG_COLOR
    )

    manage_window.resizable(
        False,
        False
    )


    tk.Label(
        manage_window,
        text="Manage Students",
        font=("Segoe UI", 22, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        pady=20
    )


    list_frame = tk.Frame(
        manage_window,
        bg=BG_COLOR
    )

    list_frame.pack(
        padx=30,
        pady=10
    )


    student_list = tk.Listbox(
        list_frame,
        font=("Segoe UI", 13),
        width=35,
        height=12
    )

    student_list.pack(
        side="left"
    )


    list_scrollbar = tk.Scrollbar(
        list_frame,
        command=student_list.yview
    )

    list_scrollbar.pack(
        side="right",
        fill="y"
    )


    student_list.config(
        yscrollcommand=list_scrollbar.set
    )


    student_files = []


    if os.path.exists("known_faces"):

        for file in os.listdir("known_faces"):

            if file.lower().endswith(
                (".jpg", ".jpeg", ".png")
            ):

                student_files.append(
                    file
                )


    student_files.sort()


    for file in student_files:

        student_name = os.path.splitext(
            file
        )[0]

        student_list.insert(
            tk.END,
            student_name
        )


    def delete_student():

        selection = student_list.curselection()


        if not selection:

            messagebox.showwarning(
                "Select Student",
                "Please select a student first.",
                parent=manage_window
            )

            return


        selected_index = selection[0]

        selected_file = student_files[
            selected_index
        ]

        selected_name = os.path.splitext(
            selected_file
        )[0]


        confirm = messagebox.askyesno(
            "Delete Student",
            f"Are you sure you want to delete {selected_name}?",
            parent=manage_window
        )


        if not confirm:

            return


        file_path = os.path.join(
            "known_faces",
            selected_file
        )


        try:

            os.remove(
                file_path
            )


            messagebox.showinfo(
                "Student Deleted",
                f"{selected_name} has been deleted.",
                parent=manage_window
            )


            student_list.delete(
                selected_index
            )

            student_files.pop(
                selected_index
            )

            update_student_count()


        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e),
                parent=manage_window
            )


    tk.Button(
        manage_window,
        text="Delete Selected Student",
        font=("Segoe UI", 13, "bold"),
        width=28,
        height=2,
        bg=DANGER_COLOR,
        fg="white",
        activebackground="#b91c1c",
        activeforeground="white",
        relief="flat",
        command=delete_student
    ).pack(
        pady=20
    )



# =========================================================
# LOGOUT
# =========================================================

def logout():

    confirm = messagebox.askyesno(
        "Logout",
        "Are you sure you want to logout?",
        parent=window
    )

    if confirm:

        window.withdraw()

        login_window.deiconify()

        username_entry.delete(
            0,
            tk.END
        )

        password_entry.delete(
            0,
            tk.END
        )

        username_entry.focus()


# =========================================================
# EXIT
# =========================================================

def exit_program():

    confirm = messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit?"
    )

    if confirm:

        window.destroy()


# =========================================================
# MAIN WINDOW TITLE
# =========================================================

tk.Label(
    window,
    text="Face Recognition",
    font=("Segoe UI", 27, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
).pack(
    pady=(25, 0)
)


tk.Label(
    window,
    text="Attendance Management System",
    font=("Segoe UI", 16),
    bg=BG_COLOR,
    fg="#6b7280"
).pack(
    pady=(2, 15)
)


# =========================================================
# SUMMARY CARDS
# =========================================================

summary_frame = tk.Frame(
    window,
    bg=BG_COLOR
)

summary_frame.pack(
    pady=5
)


def create_summary_card(
    title,
    value,
    column
):

    card = tk.Frame(
        summary_frame,
        bg=CARD_COLOR,
        width=210,
        height=100,
        bd=1,
        relief="solid"
    )

    card.grid(
        row=0,
        column=column,
        padx=8
    )

    card.grid_propagate(
        False
    )


    tk.Label(
        card,
        text=title,
        font=("Segoe UI", 10),
        bg=CARD_COLOR,
        fg="#6b7280"
    ).pack(
        pady=(15, 2)
    )


    label = tk.Label(
        card,
        text=value,
        font=("Segoe UI", 23, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    )

    label.pack()


    return label


count_label = create_summary_card(
    "Registered Students",
    "0",
    0
)


total_records_label = create_summary_card(
    "Total Records",
    "0",
    1
)


today_label = create_summary_card(
    "Today's Attendance",
    "0",
    2
)


# =========================================================
# UPDATE DATA
# =========================================================

update_student_count()

update_attendance_summary()


# =========================================================
# MAIN BUTTON HELPER
# =========================================================

def create_main_button(
    text,
    command,
    bg=BUTTON_COLOR
):

    button = tk.Button(
        window,
        text=text,
        font=("Segoe UI", 13, "bold"),
        width=32,
        height=2,
        bg=bg,
        fg="white",
        activebackground=BUTTON_HOVER,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=command
    )

    button.pack(
        pady=6
    )

    return button


# =========================================================
# START ATTENDANCE
# =========================================================

create_main_button(
    "▶  Start Attendance",
    start_attendance
)


# =========================================================
# ADD STUDENT
# =========================================================

tk.Label(
    window,
    text="Add New Student",
    font=("Segoe UI", 16, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
).pack(
    pady=(15, 5)
)


name_entry = tk.Entry(
    window,
    font=("Segoe UI", 13),
    width=32,
    justify="center"
)

name_entry.pack(
    pady=5
)


tk.Button(
    window,
    text="📷  Add Student Photo",
    font=("Segoe UI", 13, "bold"),
    width=32,
    height=2,
    bg=GREEN_COLOR,
    fg="white",
    activebackground="#15803d",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=add_student
).pack(
    pady=6
)


# =========================================================
# DASHBOARD
# =========================================================

create_main_button(
    "📊  Dashboard",
    dashboard
)


# =========================================================
# VIEW ATTENDANCE
# =========================================================

create_main_button(
    "📋  View Attendance",
    view_attendance
)


# =========================================================
# MANAGE STUDENTS
# =========================================================

create_main_button(
    "👨‍🎓  Manage Students",
    manage_students
)





# =========================================================
# LOGOUT
# =========================================================

tk.Button(
    window,
    text="🔒  Logout",
    font=("Segoe UI", 13, "bold"),
    width=32,
    height=2,
    bg=ORANGE_COLOR,
    fg="white",
    activebackground="#c2410c",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=logout
).pack(
    pady=6
)


# =========================================================
# EXIT
# =========================================================

tk.Button(
    window,
    text="✕  Exit",
    font=("Segoe UI", 13, "bold"),
    width=32,
    height=2,
    bg=DANGER_COLOR,
    fg="white",
    activebackground="#b91c1c",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=exit_program
).pack(
    pady=6
)


# =========================================================
# FOOTER
# =========================================================

tk.Label(
    window,
    text="Face Recognition Attendance System",
    font=("Segoe UI", 9),
    bg=BG_COLOR,
    fg="#6b7280"
).pack(
    side="bottom",
    pady=10
)


# =========================================================
# LOGIN FUNCTION
# =========================================================

def login():

    username = username_entry.get().strip()

    password = password_entry.get().strip()


    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

        login_window.withdraw()

        window.deiconify()

        update_student_count()

        update_attendance_summary()

    else:

        messagebox.showerror(
            "Login Failed",
            "Invalid username or password.",
            parent=login_window
        )

        password_entry.delete(
            0,
            tk.END
        )

        password_entry.focus()


# =========================================================
# SHOW / HIDE PASSWORD
# =========================================================

def toggle_password():

    if password_entry.cget("show") == "*":

        password_entry.config(
            show=""
        )

        eye_button.config(
            text="🙈"
        )

    else:

        password_entry.config(
            show="*"
        )

        eye_button.config(
            text="👁️"
        )


# =========================================================
# LOGIN WINDOW
# =========================================================

login_window = tk.Toplevel()

login_window.title(
    "Admin Login"
)

login_window.geometry(
    "450x520"
)

login_window.configure(
    bg=BG_COLOR
)

login_window.resizable(
    False,
    False
)


# =========================================================
# CLOSE LOGIN
# =========================================================

def close_login():

    window.destroy()


login_window.protocol(
    "WM_DELETE_WINDOW",
    close_login
)


# =========================================================
# LOGIN DESIGN
# =========================================================

tk.Label(
    login_window,
    text="🔐",
    font=("Segoe UI", 40),
    bg=BG_COLOR
).pack(
    pady=(30, 5)
)


tk.Label(
    login_window,
    text="Admin Login",
    font=("Segoe UI", 25, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
).pack(
    pady=5
)


tk.Label(
    login_window,
    text="Face Recognition Attendance System",
    font=("Segoe UI", 11),
    bg=BG_COLOR,
    fg="#6b7280"
).pack(
    pady=(0, 25)
)


# =========================================================
# USERNAME
# =========================================================

tk.Label(
    login_window,
    text="Username",
    font=("Segoe UI", 11, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
).pack(
    pady=(5, 5)
)


username_entry = tk.Entry(
    login_window,
    font=("Segoe UI", 13),
    width=28,
    justify="center"
)

username_entry.pack(
    ipady=7,
    pady=5
)


# =========================================================
# PASSWORD
# =========================================================

tk.Label(
    login_window,
    text="Password",
    font=("Segoe UI", 11, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
).pack(
    pady=(15, 5)
)


password_frame = tk.Frame(
    login_window,
    bg=BG_COLOR
)

password_frame.pack(
    pady=5
)


password_entry = tk.Entry(
    password_frame,
    font=("Segoe UI", 13),
    width=24,
    justify="center",
    show="*"
)

password_entry.grid(
    row=0,
    column=0,
    ipady=7
)


eye_button = tk.Button(
    password_frame,
    text="👁️",
    font=("Segoe UI", 11),
    width=4,
    height=1,
    relief="flat",
    bg=BG_COLOR,
    activebackground=BG_COLOR,
    cursor="hand2",
    command=toggle_password
)

eye_button.grid(
    row=0,
    column=1,
    padx=5
)


# =========================================================
# LOGIN BUTTON
# =========================================================

tk.Button(
    login_window,
    text="🔓  Login",
    font=("Segoe UI", 13, "bold"),
    width=25,
    height=2,
    bg=BUTTON_COLOR,
    fg="white",
    activebackground=BUTTON_HOVER,
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=login
).pack(
    pady=25
)


# =========================================================
# LOGIN INFORMATION
# =========================================================

tk.Label(
    login_window,
    text="Default Username: admin",
    font=("Segoe UI", 9),
    bg=BG_COLOR,
    fg="#6b7280"
).pack(
    pady=2
)


tk.Label(
    login_window,
    text="Password: 1234",
    font=("Segoe UI", 9),
    bg=BG_COLOR,
    fg="#6b7280"
).pack(
    pady=2
)


# =========================================================
# ENTER KEY LOGIN
# =========================================================

password_entry.bind(
    "<Return>",
    lambda event: login()
)


username_entry.focus()


# =========================================================
# START APPLICATION
# =========================================================

window.mainloop()