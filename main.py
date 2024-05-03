import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import customtkinter as ctk

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("نظام تقييم الاداء الالكتروني")
        self.master.geometry('400x350')
        self.master.resizable(False, False)

        self.welcome_label = tk.Label(master, text="نظام تقييم اداء تدريسي\n كلية علوم الحاسوب والرياضيات", fg='#ff6600', bg='#141E46', font=('thesans', 20))
        self.welcome_label.pack(pady=10, padx=10)

        self.username_label = tk.Label(master, text="اسم المستخدم", bg='#141E46', fg="white", font=('thesans', 18))
        self.username_label.pack(pady=10, padx=10)
        self.username_entry = tk.Entry(master, bd=1, relief='solid', font=('thesans', 18))
        self.username_entry.pack()

        self.password_label = tk.Label(master, text="كلمة المرور", bg='#141E46', fg='white', font=('thesans', 18))
        self.password_label.pack(pady=10, padx=10)
        self.password_entry = tk.Entry(master, bd=1, relief='solid', show='*', font=('thesans', 18))
        self.password_entry.pack()

        self.login_button = tk.Button(master, text="تسجيل الدخول", bg='#ff6600', fg='white', relief='flat', command=self.handle_login, font=('thesans', 18))
        self.login_button.pack(pady=10, padx=10)

        self.reminder = tk.Label(master, text="يرجى ادخال اسم المستخدم وكلمة المرور", fg='#41B06E', bg='#141E46', font=('thesans', 19))
        self.reminder.pack(pady=5)

    def handle_login(self):
        self.db = mysql.connector.connect(
            host='localhost',
            database='teachers',
            user='hamza',
            password='hamza'
        )
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Enter both Username and Password")
            return

        try:
            self.cursor = self.db.cursor()
            self.cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password,))
            record = self.cursor.fetchone()
            if record:
                self.master.withdraw()
                sidebar_window = Sidebar(self.master, self)
            else:
                messagebox.showerror("Login", "Invalid username or password")

        except Error as e:
            messagebox.showerror("Error", "Error, Please connect to the internet")
            print("Error while connecting to MySQL", e)

        finally:
            if self.db.is_connected():
                self.db.close()

#sidebar and header class
class Sidebar(ctk.CTkToplevel):
    def __init__(self, master, login_window):
        super().__init__(master)
        self.login_window = login_window
        self.geometry("600x400")
        self.title("نظام تقييم الاداء الالكتروني")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.config(bg='#DDF2FD')

        self.menu_icon = tk.PhotoImage(file='icons/menu.png')
        self.close_icon = tk.PhotoImage(file='icons/close.png')

        # Header
        header = tk.Frame(self, bg="#164863", height=60, highlightthickness=6)
        header.pack(side='top', fill='x')

        self.menu_button = tk.Button(header, bd=0, image=self.menu_icon, activebackground="#164863", fg='white', bg='#164863', font=('thesans', 20), command=self.menu_toggle)
        self.menu_button.pack(side='left')

        header_label = tk.Label(header, bg="#164863", fg='#FFC55A', text="نظام تقييم الاداء الالكتروني", font=('thesans', 20))
        header_label.pack()

        # Menu items
        self.menu_item_frame = tk.Frame(self, bg="#164863", highlightthickness=6, height=100)

        # item1_btn = tk.Button(self.menu_item_frame, text='المحور الأول')
        # item2_btn = tk.Button(self.menu_item_frame, text='المحور الثاني')
        # item3_btn = tk.Button(self.menu_item_frame, text='المحور الثالث')
        # item4_btn = tk.Button(self.menu_item_frame, text='المحور الرابع')
        result_btn = tk.Button(self.menu_item_frame, text='النتيجة النهائية')
        exit_btn = tk.Button(self.menu_item_frame, text='اغلاق التطبيق', command=exit)
        logout_btn = tk.Button(self.menu_item_frame, text='تسجيل الخروج', command=self.logout)

        #المعلومات التي تظهر في الشاشة الرئيسية
        self.info_frame = tk.Frame(self, width=500, height=500, bg='#DDF2FD', bd=0)
        self.info_frame.pack(side='top')

        username = self.login_window.username_entry.get().capitalize()
        username_label = tk.Label(self.info_frame, text=f'{username} مرحبا بك ', font=('thesans', 22))
        username_label.pack(padx=5, pady=5)

        for wed in self.info_frame.winfo_children():
            wed.configure(bg='#DDF2FD')
            
        for widget in self.menu_item_frame.winfo_children():
                widget.pack_configure(padx=10, pady=2)
                widget.configure(bd=0, font=('thesans', 16), fg='white', bg='#164863')

    def logout(self):
        self.destroy()
        self.login_window.master.deiconify()

    def exit(self):
        self.quit()

    def menu_toggle(self):
        if self.menu_button.cget('image') == str(self.menu_icon):
            self.menu_button.config(image=self.close_icon)
            self.menu_item_frame.pack(side='left', fill='y')
            self.config(bg='#9BBEC8')
            self.info_frame.pack_forget()

        elif self.menu_button.cget('image') == str(self.close_icon):
            self.info_frame.pack(side='top')
            self.config(bg='#DDF2FD')
            self.menu_button.config(image=self.menu_icon)
            self.menu_item_frame.pack_forget()


ctk.set_appearance_mode('dark')
root = ctk.CTk()
root.config(bg='#141E46')
root.iconbitmap('icons/form.ico')
loginwindow = LoginWindow(root)
root.mainloop()
