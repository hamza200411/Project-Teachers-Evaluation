import tkinter as tk
from tkinter import messagebox
import mysql.connector
import customtkinter as ctk
from tkinter import ttk

db = mysql.connector.connect(
    host='localhost',
    database='teachers',
    user='hamza',
    password='hamza'
)

cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS `teachers`")
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, fullname VARCHAR(255), username VARCHAR(255), college VARCHAR(255), department VARCHAR(200), password VARCHAR(255), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

def register():
    fullname = fullname_entry.get()
    username = username_entry.get()
    college = college_name_entry.get()
    department = dept_entry.get()
    password = password_entry.get()
    password2 = password_entry2.get()

    if not fullname or not username or not college or not department:
        messagebox.showerror("Error", "Please fill all fields")
        return

    if not password:
        messagebox.showerror("Error", "Please enter password")
        return

    if not password2:
        messagebox.showerror("Error", "Please confirm password")
        return

    if password != password2:
        messagebox.showerror("Error", "Password does not match")
        return
    # Check if username already exists
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        messagebox.showerror("Error", "Username already exists.")
        return

    # Insert new user into the database
    cursor.execute("INSERT INTO users (fullname, username, college, department, password) VALUES (%s, %s, %s, %s, %s)", (fullname, username, college, department, password))
    db.commit()

    messagebox.showinfo("Success", "Registration successful.")

    # Clear the entry fields after registration
    fullname_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    college_name_entry.delete(0, tk.END)
    dept_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    password_entry2.delete(0, tk.END)

root = ctk.CTk()
root.config(bg='#141E46')
root.geometry("440x390")
root.resizable(False, False)
root.title("تسجيل تدريسي جديد")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

register_frame = tk.Frame(root, bg='#141E46')
register_frame.grid(row=0, column=0)

welcome_label = tk.Label(register_frame, text="تسجيل تدريسي جديد", fg='#ff6600', bg='#141E46', font=('thesans', 20))
welcome_label.grid(row=0, column=0, padx=6, pady=6, columnspan=2)

fullname_label = tk.Label(register_frame, text="الاسم الكامل", bg='#141E46', fg="white", font=('thesans', 18))
fullname_label.grid(row=1, column=1, padx=6, pady=6)
fullname_entry = tk.Entry(register_frame, bd=1, relief='solid', font=('thesans', 18))
fullname_entry.grid(row=2, column=1, padx=6, pady=6)

username_label = tk.Label(register_frame, text="اسم المستخدم", bg='#141E46', fg="white", font=('thesans', 18))
username_label.grid(row=1, column=0, padx=6, pady=6)
username_entry = tk.Entry(register_frame, bd=1, relief='solid', font=('thesans', 18))
username_entry.grid(row=2, column=0, padx=6, pady=6)

college_name_label = tk.Label(register_frame, text="الكلية", bg='#141E46', fg="white", font=('thesans', 18))
college_name_label.grid(row=3, column=0, padx=6, pady=6)
colleges = ['Computer Science and Mathematics']
college_name_entry = ttk.Combobox(register_frame, values=colleges, font=('thesans', 18))
college_name_entry.grid(row=4, column=0, padx=6, pady=6)

dept = ['Networks', 'CyberSecurity', 'Computer Science']
dept_label = tk.Label(register_frame, text="القسم", bg='#141E46', fg="white", font=('thesans', 18))
dept_label.grid(row=3, column=1, padx=6, pady=6)
dept_entry = ttk.Combobox(register_frame, values=dept, font=('thesans', 18))
dept_entry.grid(row=4, column=1, padx=6, pady=6)

password_label = tk.Label(register_frame, text="كلمة المرور", bg='#141E46', fg='white', font=('thesans', 18))
password_label.grid(row=5, column=1, padx=6, pady=6)
password_entry = tk.Entry(register_frame, bd=1, relief='solid', show='*', font=('thesans', 18))
password_entry.grid(row=6, column=1, padx=6, pady=6)

password_label2 = tk.Label(register_frame, text="تأكيد كلمة المرور", bg='#141E46', fg='white', font=('thesans', 18))
password_label2.grid(row=5, column=0, padx=6, pady=6)
password_entry2 = tk.Entry(register_frame, bd=1, relief='solid', show='*', font=('thesans', 18))
password_entry2.grid(row=6, column=0, padx=6, pady=6)

register_button = tk.Button(register_frame, text="تسجيل", width=18, command=register, bg='#ff6600', fg='white', relief='flat', font=('thesans', 18))
register_button.grid(row=7, column=0, padx=6, pady=6, columnspan=2)

root.mainloop()
db.close()