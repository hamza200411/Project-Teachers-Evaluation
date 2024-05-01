import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import customtkinter as ctk

root = ctk.CTk()
root.title("تسجيل دخول المشرف")
root.config(bg='#141E46')
root.geometry("380x380")
root.resizable(False, False)

login_frame = tk.Frame(root, bg='#141E46')
login_frame.place(relx=0.5, rely=0.5, anchor='center')

welcome_label = tk.Label(login_frame, text="تسجيل دخول المشرفين\n لنظام تقييم اداء التدريسيين", fg='#ff6600', bg='#141E46', font=('thesans', 20))
welcome_label.pack(pady=10, padx=10)

username_label = tk.Label(login_frame, text="اسم المستخدم", bg='#141E46', fg="white", font=('thesans', 18))
username_label.pack(pady=10, padx=10)
username_entry = tk.Entry(login_frame, bd=1, relief='solid', font=('thesans', 18))
username_entry.pack()

password_label = tk.Label(login_frame, text="كلمة المرور", bg='#141E46', fg='white', font=('thesans', 18))
password_label.pack(pady=10, padx=10)
password_entry = tk.Entry(login_frame, bd=1, relief='solid', show='*', font=('thesans', 18))
password_entry.pack()

login_button = tk.Button(login_frame, text="تسجيل الدخول", bg='#ff6600', fg='white', relief='flat', font=('thesans', 18))
login_button.pack(pady=10, padx=10)

db = mysql.connector.connect(
            host='localhost',
            database='teachers',
            user='hamza',
            password='hamza'
        )
cursor = db.cursor()

def handle_login():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Enter both Username and Password")
        return

    try:
        cursor.execute("SELECT * FROM admins WHERE username=%s AND password=%s", (username, password,))
        record = cursor.fetchone()

        if record:
            messagebox.showinfo("Login", "Login successful!")
        else:
            messagebox.showerror("Login", "Invalid username or password")

    except Error as e:
        messagebox.showerror("Error", "Error, Please connect to the internet")
        print("Error while connecting to MySQL", e)

        if db.is_connected():
            cursor.close()
            db.close()

login_button.config(command=handle_login)

root.mainloop()
