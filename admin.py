import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import customtkinter as ctk
import configparser

def load_database():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return {
        'host': config['database']['host'],
        'port': config['database'].getint('port'),
        'user': config['database']['user'],
        'password': config['database']['password'],
        'database': config['database']['database']
    }


def database_connection():
    db_config = load_database()
    return mysql.connector.connect(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )

def create_tables():
    connection = database_connection()
    cursor = connection.cursor()

    # إنشاء جدول users
    create_users_table = """
    CREATE TABLE IF NOT EXISTS `users` (
      `id` int NOT NULL AUTO_INCREMENT,
      `fullname` varchar(100) NOT NULL,
      `username` varchar(100) NOT NULL,
      `college` varchar(255) DEFAULT NULL,
      `department` varchar(100) DEFAULT NULL,
      `password` varchar(255) NOT NULL,
      `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
      `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      PRIMARY KEY (`id`),
      UNIQUE KEY `username` (`username`)
    );
    """

    # إنشاء جدول admin
    create_admin_table = """
    CREATE TABLE IF NOT EXISTS `admin` (
      `id` int NOT NULL AUTO_INCREMENT,
      `username` varchar(100) NOT NULL,
      `password` varchar(255) NOT NULL,
      `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (`id`),
      UNIQUE KEY `username` (`username`)
    );
    """

    # إنشاء جدول results
    create_results_table = """
    CREATE TABLE IF NOT EXISTS `results` (
      `id` int NOT NULL AUTO_INCREMENT,
      `user_id` int NOT NULL,
      `side_one_score` int DEFAULT NULL,
      `side_two_score` int DEFAULT NULL,
      `side_three_score` int DEFAULT NULL,
      `side_four_score` int DEFAULT NULL,
      `side_fifth_score` int DEFAULT NULL,
      `total_score` int DEFAULT NULL,
      `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
      `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      PRIMARY KEY (`id`),
      FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
    );
    """

    try:
        cursor.execute(create_users_table)
        cursor.execute(create_admin_table)
        cursor.execute(create_results_table)
        connection.commit()
    except Error as e:
        messagebox.showerror("خطأ", e)
    finally:
        cursor.close()
        connection.close()


create_tables()

def insert_admin():
    try:
        connection = database_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM admin where username = 'admin'")
        user = cursor.fetchone()
        if user:
            return
        else:
            insert_user = """
            INSERT INTO admin (username, password) VALUES ('admin', '123');
            """
            cursor.execute(insert_user)
            connection.commit()

    except Error as e:
        messagebox.showerror("خطأ", e)
    finally:
        cursor.close()
        connection.close()

insert_admin()

class loginwindow:
    def __init__(self, master):
        self.master = master
        self.master.title("تسجيل دخول المشرف")
        self.master.config(bg='#141E46')
        self.master.geometry("360x340+600+200")
        self.master.resizable(False, False)

        self.login_frame = tk.Frame(master, bg='#141E46')
        self.login_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.welcome_label = tk.Label(self.login_frame, text="تسجيل دخول المشرفين\n لنظام تقييم اداء التدريسيين", fg='#ff6600', bg='#141E46', font=('thesans', 20))
        self.welcome_label.pack(pady=10, padx=10)

        self.username_label = tk.Label(self.login_frame, text="اسم المستخدم", bg='#141E46', fg="white", font=('thesans', 18))
        self.username_label.pack(pady=10, padx=10)
        self.username_var = tk.StringVar()
        self.username_entry = tk.Entry(self.login_frame, textvariable=self.username_var, bd=1, relief='solid', font=('thesans', 18))
        self.username_entry.pack()

        self.password_label = tk.Label(self.login_frame, text="كلمة المرور", bg='#141E46', fg='white', font=('thesans', 18))
        self.password_label.pack(pady=10, padx=10)
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(self.login_frame, textvariable=self.password_var, bd=1, relief='solid', show='•', font=('thesans', 18))
        self.password_entry.pack()

        self.login_button = tk.Button(self.login_frame, text="تسجيل الدخول", bg='#ff6600', fg='white', relief='flat', font=('thesans', 18))
        self.login_button.pack(pady=10, padx=10)

        self.db = database_connection()
        self.cursor = self.db.cursor()

        def handle_login():
            username = self.username_entry.get()
            password = self.password_entry.get()

            if not username or not password:
                messagebox.showerror("خطأ", "الرجاء ادخال اسم المستخدم وكلمة المرور")
                return

            try:
                self.cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password,))
                record = self.cursor.fetchone()

                if record:
                    self.master.withdraw()
                    adminwindow = Admin_Window(self.master, self)
                else:
                    messagebox.showerror("تسجيل الدخول", "كلمة المرور او اسم المستخدم غير صحيح")

            except Error as e:
                messagebox.showerror("خطأ", f"الرجاء الاتصال بالانترنت \n {e}")

        self.login_button.config(command=handle_login)

class Admin_Window(ctk.CTkToplevel):
    def __init__(self, master, loginwindow):
        super().__init__(master)
        self.loginwindow = loginwindow
        self.title('المشرف')
        self.geometry('600x400+500+200')
        self.rowconfigure((0, 2, 3, 4, 5), weight=1)
        self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.config(bg='#141E46')
        self.resizable(False, False)

        shortcut_bar = tk.Frame(self, bg='#141E46')
        shortcut_bar.grid(row=0, column=0, sticky='n', columnspan=6, pady=4)

        welcome_label = tk.Label(shortcut_bar, text='لوحة التحكم', bg='#141E46', fg='#41B06E', font=('thesans', 24))
        welcome_label.grid(row=0, column=1, pady=6)

        new_teacher_btn = tk.Button(shortcut_bar, text="تسجيل تدريسي جديد", bg='#FC6736', fg='white', font=('thesans', 17))
        new_teacher_btn.grid(row=1, column=2)

        search_result_btn = tk.Button(shortcut_bar, text="البحث عن تقييم التدريسيين", bg='#FC6736', fg='white', font=('thesans', 17))
        search_result_btn.grid(row=1, column=0)

        view_teacher_btn = tk.Button(shortcut_bar, text="قاعدة بيانات التدريسين ", bg='#FC6736', fg='white', font=('thesans', 17))
        view_teacher_btn.grid(row=1, column=1)

        for widget in shortcut_bar.winfo_children():
            widget.grid_configure(padx=2)
            widget.configure(bd=0, activebackground='#FC6736', activeforeground='white')

        def move_to_new_teacher():
            self.withdraw()
            new_teacher(self)

        def view_teachers():
            self.withdraw()
            show_teachers(self)

        def view_results():
            self.withdraw()
            show_results(self)

        new_teacher_btn.config(command=lambda: move_to_new_teacher())
        view_teacher_btn.config(command=lambda: view_teachers())
        search_result_btn.config(command=lambda: view_results())

        self.return_btn = tk.Button(self, text='تسجيل الخروج', bg='red', fg='white', font=('thesans', 15))
        self.return_btn.grid(row=5, column=0, pady=10)

        dev_label = tk.Label(self, text='تطوير وبرمجة: حمزة محمد , ليث صدام', bg='#141E46', fg='#41B06E', font=('thesans', 13))
        dev_label.grid(row=5, column=5, pady=10)

        def return_home():
            self.master.deiconify()
            self.destroy()
        self.return_btn.config(command=lambda: return_home())

class new_teacher(ctk.CTkToplevel):
    def __init__(self, Admin_Window):
        super().__init__(Admin_Window)
        self.Admin_Window = Admin_Window
        self.config(bg='#141E46')
        self.geometry("440x390+600+200")
        self.resizable(False, False)
        self.title("تسجيل تدريسي جديد")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.db = database_connection()
        self.cursor = self.db.cursor()

        register_frame = tk.Frame(self, bg='#141E46')
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
        password_entry = tk.Entry(register_frame, bd=1, relief='solid', show='•', font=('thesans', 18))
        password_entry.grid(row=6, column=1, padx=6, pady=6)

        password_label2 = tk.Label(register_frame, text="تأكيد كلمة المرور", bg='#141E46', fg='white', font=('thesans', 18))
        password_label2.grid(row=5, column=0, padx=6, pady=6)
        password_entry2 = tk.Entry(register_frame, bd=1, relief='solid', show='•', font=('thesans', 18))
        password_entry2.grid(row=6, column=0, padx=6, pady=6)

        self.register_button = tk.Button(register_frame, text="تسجيل", width=18, bg='#ff6600', fg='white', relief='flat', font=('thesans', 18))
        self.register_button.grid(row=7, column=0, padx=5, pady=5, columnspan=1)

        self.return_btn = tk.Button(register_frame, text='العودة الى الرئيسية',  width=20, bg='#ff6600', fg='white', relief='flat', font=('thesans', 18))
        self.return_btn.grid(row=7, column=1, padx=5, pady=5, columnspan=1)

        def return_home():
            self.master.deiconify()
            self.destroy()

        self.return_btn.config(command=lambda: return_home())

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
            self.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = self.cursor.fetchone()

            if existing_user:
                messagebox.showerror("Error", "Username already exists.")
                return

            # Insert new user into the database
            self.cursor.execute("INSERT INTO users (fullname, username, college, department, password) VALUES (%s, %s, %s, %s, %s)", (fullname, username, college, department, password))
            messagebox.showinfo('success', 'تم التسجيل بنجاح')
            self.db.commit()

            # Clear the entry fields
            fullname_entry.delete(0, tk.END)
            username_entry.delete(0, tk.END)
            college_name_entry.delete(0, tk.END)
            dept_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
            password_entry2.delete(0, tk.END)

            if self.db.is_connected():
                self.db.close()
                self.cursor.close()
        self.register_button.config(command=register)

class show_teachers(ctk.CTkToplevel):
    def __init__(self, Admin_Window):
        super().__init__(Admin_Window)
        self.Admin_Window = Admin_Window
        self.config(bg='#141E46')
        self.geometry("650x400+600+200")
        self.resizable(False, False)
        self.title("قاعدة بيانات التدريسين")
        # self.rowconfigure(1, weight=1)
        # self.columnconfigure(1, weight=1)
        self.db = database_connection()

        self.cursor = self.db.cursor()
        self.cursor.execute("SELECT * FROM users")
        records = self.cursor.fetchall()

        search_frame = tk.Frame(self, bg='#141E46')
        search_frame.grid(row=0, column=0)

        self.search_label = tk.Label(search_frame, text="قاعدة بيانات التدريسين", fg='#ff6600', bg='#141E46', font=('thesans', 20))
        self.search_label.grid(row=0, column=0, padx=6, pady=6, columnspan=2)

        self.search_entry = tk.Entry(search_frame, bd=1, relief='solid', font=('thesans', 18))
        self.search_entry.grid(row=1, column=0, padx=6, pady=6)

        self.search_button = tk.Button(search_frame, text="بحث", width=4, bg='#ff6600', fg='white', relief='flat', font=('thesans', 18))
        self.search_button.grid(row=1, column=1, padx=5, pady=5)

        self.tree_frame = tk.Frame(self, bg='#141E46')
        self.tree_frame.grid(row=1, column=0)

        self.tree = ttk.Treeview(self.tree_frame, columns=(1, 2, 3, 4, 5), show='headings', height=10)
        self.tree.grid(row=0, column=0)
        self.tree.heading(1, text='رقم الهوية')
        self.tree.heading(2, text='الاسم الكامل')
        self.tree.heading(3, text='اسم المستخدم')
        self.tree.heading(4, text='الكلية')
        self.tree.heading(5, text='القسم')

        for record in records:
            self.tree.insert('', 'end', values=record)

        def search_for_teacher():
            self.search = self.search_entry.get()
            self.cursor.execute("SELECT * FROM users WHERE fullname LIKE %s", ('%' + self.search + '%',))
            records = self.cursor.fetchall()
            if records == []:
                messagebox.showinfo('Not Found', 'No record found')
            else:
                for i in self.tree.get_children():
                    self.tree.delete(i)
                for record in records:
                    self.tree.insert('', 'end', values=record)

        self.search_button.config(command=search_for_teacher)

        self.return_btn = tk.Button(self.tree_frame, text='العودة الى الرئيسية',  width=20, bg='#ff6600', fg='white', relief='flat', font=('thesans', 18))
        self.return_btn.grid(row=1, column=0, padx=5, pady=5)

        def return_home():
            self.master.deiconify()
            self.destroy()

        self.return_btn.config(command=lambda: return_home())

        if self.db.is_connected():
            self.db.close()
            self.cursor.close()

class show_results(ctk.CTkToplevel):
    def __init__(self, Admin_Window):
        super().__init__(Admin_Window)
        self.Admin_Window = Admin_Window
        self.config(bg="#141E46")
        self.geometry("1050x400+500+200")
        self.resizable(False, False)
        self.title("عرض تقييم التدريسيين")

        self.db = database_connection()
        self.cursor = self.db.cursor()
        self.cursor.execute("SELECT * FROM results")
        records = self.cursor.fetchall()

        search_frame = tk.Frame(self, bg='#141E46')
        search_frame.grid(row=0, column=0)

        self.search_label = tk.Label(search_frame, text="نتائج تقييم التدريسين", fg='#ff6600', bg='#141E46',
                                     font=('thesans', 20))
        self.search_label.grid(row=0, column=0, padx=6, pady=6, columnspan=2)

        self.search_entry = tk.Entry(search_frame, bd=1, relief='solid', font=('thesans', 18))
        self.search_entry.grid(row=1, column=0, padx=6, pady=6)

        self.search_button = tk.Button(search_frame, text="بحث", width=4, bg='#ff6600', fg='white', relief='flat',
                                       font=('thesans', 18))
        self.search_button.grid(row=1, column=1, padx=5, pady=5)

        self.tree_frame = tk.Frame(self, bg='#141E46')
        self.tree_frame.grid(row=1, column=0)

        self.tree = ttk.Treeview(self.tree_frame, columns=(1, 2, 4, 5, 6, 7, 8, 9), show='headings', height=10)
        self.tree.grid(row=0, column=0)
        self.tree.heading(1, text='ID')
        self.tree.heading(2, text='User ID')
        self.tree.heading(4, text='المحور الاول')
        self.tree.heading(5, text='المحور الثاني')
        self.tree.heading(6, text='المحور الثالث')
        self.tree.heading(7, text='المحور الرابع')
        self.tree.heading(8, text='المحور الخامس')
        self.tree.heading(9, text='النتيجة النهائية')

        for record in records:
            self.tree.insert('', 'end', values=record)

        def search_for_result():
            self.cursor = self.db.cursor()
            self.search = self.search_entry.get()
            self.cursor.execute("SELECT * FROM results WHERE results.user_id LIKE %s", ('%' + self.search + '%',))
            records = self.cursor.fetchall()
            if records == []:
                messagebox.showinfo('لا يوجد نتائج', 'لا يوجد نتائج')
            else:
                for i in self.tree.get_children():
                    self.tree.delete(i)
                for record in records:
                    self.tree.insert('', 'end', values=record)

        self.search_button.config(command=search_for_result())

        self.return_btn = tk.Button(self.tree_frame, text='العودة الى الرئيسية', width=20, bg='#ff6600', fg='white',
                                    relief='flat', font=('thesans', 18))
        self.return_btn.grid(row=1, column=0, padx=5, pady=5)

        self.delete_result = tk.Button(self.tree_frame, text='حذف النتيجة', width=20, bg='red', fg='white',
                                    relief='flat', font=('thesans', 18))
        self.delete_result.grid(row=2, column=0, padx=5, pady=5)

        def delete_result():
            try:
                selected_result = self.tree.selection()[0]
                item_data = self.tree.item(selected_result, 'values')
                result_id = item_data[0]
                self.tree.delete(selected_result)
                self.cursor.execute("DELETE FROM results WHERE id=%s", (result_id,))
                self.db.commit()

                messagebox.showinfo('Success', 'تم حذف النتيجة بنجاح')
            except IndexError:
                messagebox.showerror('Error', 'يرجى اختيار نتيجة لحذفها')

        self.delete_result.config(command=delete_result)

        def return_home():
            self.master.deiconify()
            self.destroy()

        self.return_btn.config(command=lambda: return_home())

ctk.set_appearance_mode('dark')
root = ctk.CTk()
root.iconbitmap('icons/form.ico')
loginwindow = loginwindow(root)
root.mainloop()
