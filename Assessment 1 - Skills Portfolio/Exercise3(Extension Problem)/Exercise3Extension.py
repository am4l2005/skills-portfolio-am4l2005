import tkinter as tk
from tkinter import messagebox
import os

# ------------------ Student ------------------
class Student:
    def __init__(self, code, name, c1, c2, c3, exam):
        self.code = int(code)
        self.name = name
        self.c1 = int(c1); self.c2 = int(c2); self.c3 = int(c3)
        self.exam = int(exam)

    def cw(self): return self.c1 + self.c2 + self.c3
    def total(self): return self.cw() + self.exam
    def pct(self): return round((self.total() / 160) * 100, 2)

    def grade(self):
        p = self.pct()
        if p >= 70: return "A"
        if p >= 60: return "B"
        if p >= 50: return "C"
        if p >= 40: return "D"
        return "F"

    def to_line(self):
        return f"{self.code},{self.name},{self.c1},{self.c2},{self.c3},{self.exam}"

# ------------------ Manager ------------------
class StudentManager:
    def __init__(self, path):
        self.path = path
        self.students = []
        self.load()

    def load(self):
        if not os.path.exists(self.path): open(self.path, "w").close()
        with open(self.path, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
        data = lines[1:] if lines and lines[0].isdigit() else lines
        st = []
        for ln in data:
            parts = ln.split(",")
            if len(parts) == 6:
                st.append(Student(*parts))
        self.students = st

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(str(len(self.students)) + "\n")
            for s in self.students:
                f.write(s.to_line() + "\n")

    def by_code(self, code):
        for s in self.students:
            if s.code == code: return s
        return None

# ------------------ Add Student Popup ------------------
class AddStudentPopup(tk.Toplevel):
    def __init__(self, parent, on_submit):
        super().__init__(parent)
        self.title("Add Student")
        self.geometry("300x350")
        self.on_submit = on_submit

        self.entries = {}
        fields = ["Code", "Name", "CW1", "CW2", "CW3", "Exam"]
        for t in fields:
            tk.Label(self, text=t, font=("Segoe UI", 10)).pack(anchor="w", padx=10, pady=3)
            entry = tk.Entry(self, font=("Segoe UI", 10))
            entry.pack(fill="x", padx=10)
            self.entries[t] = entry

        tk.Button(self, text="Submit", bg="#4c57ff", fg="white",
                  command=self.submit).pack(pady=10)

    def submit(self):
        try:
            code = int(self.entries["Code"].get())
            name = self.entries["Name"].get()
            c1 = int(self.entries["CW1"].get())
            c2 = int(self.entries["CW2"].get())
            c3 = int(self.entries["CW3"].get())
            exam = int(self.entries["Exam"].get())
            self.on_submit(code, name, c1, c2, c3, exam)
            self.destroy()
        except:
            messagebox.showerror("Error", "Invalid input.")

# ------------------ App ------------------
class App:
    def __init__(self, root, manager):
        self.root = root
        self.m = manager
        self.sort_asc = True  # Track sort order

        root.title("Student Manager - Simple Edition")
        root.geometry("850x500")
        root.config(bg="#f2f2f2")

        tk.Label(root, text="Student Manager", bg="#4c57ff", fg="white",
                 font=("Segoe UI", 18, "bold"), pady=10).pack(fill="x")

        # Main container
        main = tk.Frame(root, bg="#f2f2f2")
        main.pack(fill="both", expand=True, padx=10, pady=10)

        # LEFT: LISTBOX
        left = tk.Frame(main, bg="#f2f2f2")
        left.pack(side="left", fill="y")
        tk.Label(left, text="Students", font=("Segoe UI", 12, "bold"), bg="#f2f2f2").pack(anchor="w")
        self.listbox = tk.Listbox(left, width=32, height=23, font=("Segoe UI", 10))
        self.listbox.pack()
        self.listbox.bind("<<ListboxSelect>>", self.select_student)

        # RIGHT: OUTPUT
        right = tk.Frame(main, bg="#f2f2f2")
        right.pack(side="right", fill="both", expand=True)
        tk.Label(right, text="Output", font=("Segoe UI", 12, "bold"), bg="#f2f2f2").pack(anchor="w")
        self.output = tk.Text(right, wrap="word", height=20, font=("Segoe UI", 10))
        self.output.pack(fill="both", expand=True)

        # MENU BUTTONS
        menu = tk.Frame(root, bg="#f2f2f2")
        menu.pack(fill="x", pady=6)
        sbtn = dict(bg="#4c57ff", fg="white", font=("Segoe UI", 10, "bold"), width=16)
        tk.Button(menu, text="View All", command=self.view_all, **sbtn).pack(side="left", padx=4)
        tk.Button(menu, text="View Individual", command=self.view_single, **sbtn).pack(side="left", padx=4)
        tk.Button(menu, text="Highest Score", command=self.view_highest, **sbtn).pack(side="left", padx=4)
        tk.Button(menu, text="Lowest Score", command=self.view_lowest, **sbtn).pack(side="left", padx=4)
        tk.Button(menu, text="Sort by Total", command=self.sort_total, **sbtn).pack(side="left", padx=4)
        tk.Button(menu, text="Add Student", command=self.add_student, **sbtn).pack(side="left", padx=4)
        tk.Button(menu, text="Delete Student", command=self.delete_student, **sbtn).pack(side="left", padx=4)

        self.refresh()

    # ---------------- Utils ----------------
    def write(self, txt):
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("end", txt)
        self.output.config(state="disabled")

    def refresh(self):
        self.listbox.delete(0, "end")
        for s in self.m.students:
            self.listbox.insert("end", f"{s.code} - {s.name}")

    def format_s(self, s):
        return (f"Name: {s.name}\n"
                f"Code: {s.code}\n"
                f"Coursework: {s.cw()}/60\n"
                f"Exam: {s.exam}/100\n"
                f"Total: {s.total()}/160\n"
                f"Percentage: {s.pct()}%\n"
                f"Grade: {s.grade()}\n")

    # ---------------- Features ----------------
    def select_student(self, e=None):
        try: idx = self.listbox.curselection()[0]
        except: return
        s = self.m.students[idx]
        self.write(self.format_s(s))

    def view_all(self):
        if not self.m.students: self.write("No students available."); return
        out = ""; total = 0
        for s in self.m.students:
            out += self.format_s(s) + "-"*40 + "\n"; total += s.pct()
        avg = round(total / len(self.m.students), 2)
        out += f"\nTotal Students: {len(self.m.students)}\nAverage Percentage: {avg}%"
        self.write(out)

    def view_single(self):
        from tkinter import simpledialog
        code = simpledialog.askinteger("Find", "Enter student code:")
        if code is None: return
        s = self.m.by_code(code)
        if not s: messagebox.showinfo("Not found", "No student with that code."); return
        self.write(self.format_s(s))

    def view_highest(self):
        if not self.m.students: return
        s = max(self.m.students, key=lambda x: x.total())
        self.write("Highest Scoring Student:\n\n" + self.format_s(s))

    def view_lowest(self):
        if not self.m.students: return
        s = min(self.m.students, key=lambda x: x.total())
        self.write("Lowest Scoring Student:\n\n" + self.format_s(s))

    # ---------------- Sort / Add / Delete ----------------
    def sort_total(self):
        self.m.students.sort(key=lambda s: s.total(), reverse=not self.sort_asc)
        self.sort_asc = not self.sort_asc
        self.m.save()
        self.refresh()
        order = "ascending" if self.sort_asc else "descending"
        self.write(f"Students sorted by total score ({order}).")

    def add_student(self):
        AddStudentPopup(self.root, self._add_student_submit)

    def _add_student_submit(self, code, name, c1, c2, c3, exam):
        if self.m.by_code(code):
            messagebox.showerror("Error", "Code already exists."); return
        s = Student(code, name, c1, c2, c3, exam)
        self.m.students.append(s)
        self.m.save()
        self.refresh()
        messagebox.showinfo("Added", "Student added successfully.")

    def delete_student(self):
        from tkinter import simpledialog
        code = simpledialog.askinteger("Delete", "Student code:")
        if code is None: return
        s = self.m.by_code(code)
        if not s: messagebox.showerror("Error", "Student not found."); return
        self.m.students.remove(s)
        self.m.save()
        self.refresh()
        messagebox.showinfo("Deleted", "Student removed.")

# ---------------- MAIN ----------------
def main():
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "studentMarks.txt")
    mgr = StudentManager(path)
    root = tk.Tk()
    App(root, mgr)
    root.mainloop()

if __name__ == "__main__":
    main()
