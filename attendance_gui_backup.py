import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import subprocess
import sys
import os
import shutil
import csv
from datetime import datetime
from openpyxl import Workbook


# =========================
# Start Attendance
# =========================
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


# =========================
# Add Student
# =========================
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

    new_filename = name + extension

    destination = os.path.join(
        "known_faces",
        new_filename
    )

    # Check duplicate student
    existing_files = os.listdir(
        "known_faces"
    )

    for file in existing_files:

        existing_name = os.path.splitext(
            file
        )[0]

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


# =========================
# Update Student Count
# =========================
def update_student_count():

    count = 0

    if os.path.exists("known_faces"):

        for file in os.listdir("known_faces"):

            if file.lower().endswith(
                (".jpg", ".jpeg", ".png")
            ):

                count += 1

    count_label.config(
        text=f"Registered Students: {count}"
    )


# =========================
# Attendance Summary
# =========================
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
        text=f"Total Attendance Records: {total_records}"
    )

    today_label.config(
        text=f"Today's Attendance: {today_attendance}"
    )


# =========================
# Dashboard
# =========================
def dashboard():

    dashboard_window = tk.Toplevel(
        window
    )

    dashboard_window.title(
        "Attendance Dashboard"
    )

    dashboard_window.geometry(
        "700x600"
    )

    dashboard_window.resizable(
        False,
        False
    )


    # =========================
    # Heading
    # =========================

    heading = tk.Label(
        dashboard_window,
        text="Attendance Dashboard",
        font=(
            "Segoe UI",
            22,
            "bold"
        )
    )

    heading.pack(
        pady=20
    )


    # =========================
    # Read Data
    # =========================

    total_students = 0
    total_attendance = 0
    today_attendance = 0

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )


    # =========================
    # Count Students
    # =========================

    if os.path.exists("known_faces"):

        for file in os.listdir("known_faces"):

            if file.lower().endswith(
                (".jpg", ".jpeg", ".png")
            ):

                total_students += 1


    # =========================
    # Count Attendance
    # =========================

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

                        total_attendance += 1

                        if row[1].strip() == today:

                            today_attendance += 1

        except Exception:

            pass


    # =========================
    # Attendance Percentage
    # =========================

    if total_students > 0:

        attendance_percentage = (
            today_attendance /
            total_students
        ) * 100

    else:

        attendance_percentage = 0


    # =========================
    # Dashboard Cards
    # =========================

    students_frame = tk.Frame(
        dashboard_window,
        bd=2,
        relief="groove",
        width=550,
        height=70
    )

    students_frame.pack(
        pady=8
    )

    students_frame.pack_propagate(
        False
    )

    tk.Label(
        students_frame,
        text=f"Registered Students: {total_students}",
        font=(
            "Segoe UI",
            15,
            "bold"
        )
    ).pack(
        pady=18
    )


    attendance_frame = tk.Frame(
        dashboard_window,
        bd=2,
        relief="groove",
        width=550,
        height=70
    )

    attendance_frame.pack(
        pady=8
    )

    attendance_frame.pack_propagate(
        False
    )

    tk.Label(
        attendance_frame,
        text=f"Total Attendance Records: {total_attendance}",
        font=(
            "Segoe UI",
            15,
            "bold"
        )
    ).pack(
        pady=18
    )


    today_frame = tk.Frame(
        dashboard_window,
        bd=2,
        relief="groove",
        width=550,
        height=70
    )

    today_frame.pack(
        pady=8
    )

    today_frame.pack_propagate(
        False
    )

    tk.Label(
        today_frame,
        text=f"Today's Attendance: {today_attendance}",
        font=(
            "Segoe UI",
            15,
            "bold"
        )
    ).pack(
        pady=18
    )


    percentage_frame = tk.Frame(
        dashboard_window,
        bd=2,
        relief="groove",
        width=550,
        height=70
    )

    percentage_frame.pack(
        pady=8
    )

    percentage_frame.pack_propagate(
        False
    )

    tk.Label(
        percentage_frame,
        text=(
            f"Today's Attendance Percentage: "
            f"{attendance_percentage:.1f}%"
        ),
        font=(
            "Segoe UI",
            15,
            "bold"
        )
    ).pack(
        pady=18
    )


    # =========================
    # Show Chart
    # =========================

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
            "Attendance Status"
        )

        plt.ylabel(
            "Number of Students"
        )

        plt.tight_layout()

        plt.show()


    chart_button = tk.Button(
        dashboard_window,
        text="Show Attendance Chart",
        font=(
            "Segoe UI",
            13,
            "bold"
        ),
        width=25,
        height=2,
        command=show_chart
    )

    chart_button.pack(
        pady=15
    )


# =========================
# Export Attendance to Excel
# =========================
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


# =========================
# View Attendance
# =========================
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

    attendance_window.resizable(
        False,
        False
    )


    # =========================
    # Heading
    # =========================

    heading = tk.Label(
        attendance_window,
        text="Attendance Records",
        font=(
            "Segoe UI",
            20,
            "bold"
        )
    )

    heading.pack(
        pady=12
    )


    # =========================
    # Search Section
    # =========================

    search_frame = tk.Frame(
        attendance_window
    )

    search_frame.pack(
        pady=8
    )


    student_label = tk.Label(
        search_frame,
        text="Student:",
        font=(
            "Segoe UI",
            11,
            "bold"
        )
    )

    student_label.grid(
        row=0,
        column=0,
        padx=5
    )


    student_search = tk.Entry(
        search_frame,
        font=(
            "Segoe UI",
            11
        ),
        width=20
    )

    student_search.grid(
        row=0,
        column=1,
        padx=5
    )


    date_label = tk.Label(
        search_frame,
        text="Date:",
        font=(
            "Segoe UI",
            11,
            "bold"
        )
    )

    date_label.grid(
        row=0,
        column=2,
        padx=5
    )


    date_search = tk.Entry(
        search_frame,
        font=(
            "Segoe UI",
            11
        ),
        width=15
    )

    date_search.grid(
        row=0,
        column=3,
        padx=5
    )


    # =========================
    # Load Attendance Data
    # =========================

    attendance_data = []


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


    # =========================
    # Table
    # =========================

    table_frame = tk.Frame(
        attendance_window
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=5
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


    # =========================
    # Display Records
    # =========================

    def display_records(records):

        for item in table.get_children():

            table.delete(
                item
            )

        for record in records:

            table.insert(
                "",
                "end",
                values=record
            )


    display_records(
        attendance_data
    )


    # =========================
    # Filter Records
    # =========================

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

            student_name = record[0].lower()

            attendance_date = record[1].lower()


            student_match = (
                student_text == ""
                or student_text in student_name
            )


            date_match = (
                date_text == ""
                or date_text in attendance_date
            )


            if student_match and date_match:

                filtered_records.append(
                    record
                )


        return filtered_records


    # =========================
    # Search
    # =========================

    def search_attendance(event=None):

        filtered_records = get_current_records()

        display_records(
            filtered_records
        )


    student_search.bind(
        "<KeyRelease>",
        search_attendance
    )

    date_search.bind(
        "<KeyRelease>",
        search_attendance
    )


    # =========================
    # Buttons
    # =========================

    button_frame = tk.Frame(
        attendance_window
    )

    button_frame.pack(
        pady=8
    )


    # =========================
    # Clear Search
    # =========================

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


    clear_button = tk.Button(
        button_frame,
        text="Clear Search",
        font=(
            "Segoe UI",
            11,
            "bold"
        ),
        width=15,
        command=clear_search
    )

    clear_button.grid(
        row=0,
        column=0,
        padx=10
    )


    # =========================
    # Export Excel
    # =========================

    export_button = tk.Button(
        button_frame,
        text="Export to Excel",
        font=(
            "Segoe UI",
            11,
            "bold"
        ),
        width=18,
        command=lambda: export_to_excel(
            get_current_records(),
            attendance_window
        )
    )

    export_button.grid(
        row=0,
        column=1,
        padx=10
    )


    # =========================
    # Hint
    # =========================

    hint = tk.Label(
        attendance_window,
        text="Date format: YYYY-MM-DD",
        font=(
            "Segoe UI",
            9
        )
    )

    hint.pack(
        pady=3
    )


# =========================
# Manage Students
# =========================
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

    manage_window.resizable(
        False,
        False
    )


    heading = tk.Label(
        manage_window,
        text="Manage Students",
        font=(
            "Segoe UI",
            20,
            "bold"
        )
    )

    heading.pack(
        pady=20
    )


    list_frame = tk.Frame(
        manage_window
    )

    list_frame.pack(
        padx=30,
        pady=10
    )


    student_list = tk.Listbox(
        list_frame,
        font=(
            "Segoe UI",
            13
        ),
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


    # =========================
    # Delete Student
    # =========================

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


    delete_button = tk.Button(
        manage_window,
        text="Delete Selected Student",
        font=(
            "Segoe UI",
            13,
            "bold"
        ),
        width=28,
        height=2,
        command=delete_student
    )

    delete_button.pack(
        pady=20
    )


# =========================
# Exit
# =========================
def exit_program():

    window.destroy()


# =========================
# Main Window
# =========================

window = tk.Tk()

window.title(
    "Face Recognition Attendance System"
)

window.geometry(
    "650x820"
)

window.resizable(
    False,
    False
)


# =========================
# Style
# =========================

style = ttk.Style()

style.theme_use(
    "clam"
)


style.configure(
    "Treeview.Heading",
    font=(
        "Segoe UI",
        11,
        "bold"
    )
)


style.configure(
    "Treeview",
    font=(
        "Segoe UI",
        10
    ),
    rowheight=30
)


# =========================
# Title
# =========================

title = tk.Label(
    window,
    text="Face Recognition Attendance System",
    font=(
        "Segoe UI",
        22,
        "bold"
    )
)

title.pack(
    pady=25
)


# =========================
# Student Count
# =========================

count_label = tk.Label(
    window,
    text="Registered Students: 0",
    font=(
        "Segoe UI",
        12,
        "bold"
    )
)

count_label.pack(
    pady=5
)


# =========================
# Total Records
# =========================

total_records_label = tk.Label(
    window,
    text="Total Attendance Records: 0",
    font=(
        "Segoe UI",
        12,
        "bold"
    )
)

total_records_label.pack(
    pady=5
)


# =========================
# Today's Attendance
# =========================

today_label = tk.Label(
    window,
    text="Today's Attendance: 0",
    font=(
        "Segoe UI",
        12,
        "bold"
    )
)

today_label.pack(
    pady=5
)


# =========================
# Initial Summary
# =========================

update_student_count()

update_attendance_summary()


# =========================
# Start Attendance
# =========================

start_button = tk.Button(
    window,
    text="Start Attendance",
    font=(
        "Segoe UI",
        14
    ),
    width=30,
    height=2,
    command=start_attendance
)

start_button.pack(
    pady=10
)


# =========================
# Add Student
# =========================

add_title = tk.Label(
    window,
    text="Add New Student",
    font=(
        "Segoe UI",
        16,
        "bold"
    )
)

add_title.pack(
    pady=(20, 10)
)


name_entry = tk.Entry(
    window,
    font=(
        "Segoe UI",
        14
    ),
    width=30,
    justify="center"
)

name_entry.pack(
    pady=5
)


add_button = tk.Button(
    window,
    text="Add Student Photo",
    font=(
        "Segoe UI",
        14
    ),
    width=30,
    height=2,
    command=add_student
)

add_button.pack(
    pady=10
)


# =========================
# Dashboard
# =========================

dashboard_button = tk.Button(
    window,
    text="Dashboard",
    font=(
        "Segoe UI",
        14
    ),
    width=30,
    height=2,
    command=dashboard
)

dashboard_button.pack(
    pady=8
)


# =========================
# View Attendance
# =========================

view_button = tk.Button(
    window,
    text="View Attendance",
    font=(
        "Segoe UI",
        14
    ),
    width=30,
    height=2,
    command=view_attendance
)

view_button.pack(
    pady=8
)


# =========================
# Manage Students
# =========================

manage_button = tk.Button(
    window,
    text="Manage Students",
    font=(
        "Segoe UI",
        14
    ),
    width=30,
    height=2,
    command=manage_students
)

manage_button.pack(
    pady=8
)


# =========================
# Exit
# =========================

exit_button = tk.Button(
    window,
    text="Exit",
    font=(
        "Segoe UI",
        14
    ),
    width=30,
    height=2,
    command=exit_program
)

exit_button.pack(
    pady=8
)


# =========================
# Footer
# =========================

footer = tk.Label(
    window,
    text="Face Recognition Attendance System",
    font=(
        "Segoe UI",
        9
    )
)

footer.pack(
    side="bottom",
    pady=15
)


# =========================
# Start GUI
# =========================

window.mainloop()