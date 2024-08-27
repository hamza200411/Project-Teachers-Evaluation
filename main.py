import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
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


class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("نظام تقييم الاداء الالكتروني")
        self.master.geometry('400x350')
        self.master.resizable(False, False)

        self.welcome_label = tk.Label(master, text="نظام تقييم اداء تدريسي\n كلية علوم الحاسوب والرياضيات",
                                      fg='#ff6600', bg='#141E46', font=('thesans', 20))
        self.welcome_label.pack(pady=10, padx=10)

        self.username_label = tk.Label(master, text="اسم المستخدم", bg='#141E46', fg="white", font=('thesans', 18))
        self.username_label.pack(pady=10, padx=10)
        self.username_var = tk.StringVar()
        self.username_entry = tk.Entry(master, bd=1, relief='solid', font=('thesans', 18),
                                       textvariable=self.username_var)
        self.username_var.set('hamza')
        self.username_entry.pack()

        self.password_label = tk.Label(master, text="كلمة المرور", bg='#141E46', fg='white', font=('thesans', 18))
        self.password_label.pack(pady=10, padx=10)
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(master, bd=1, relief='solid', show='•', font=('thesans', 18),
                                       textvariable=self.password_var)
        self.password_var.set('123')
        self.password_entry.pack()

        self.login_button = tk.Button(master, text="تسجيل الدخول", bg='#ff6600', fg='white', relief='flat',
                                      command=self.handle_login, font=('thesans', 18))
        self.login_button.pack(pady=10, padx=10)

        self.reminder = tk.Label(master, text="يرجى ادخال اسم المستخدم وكلمة المرور", fg='#41B06E', bg='#141E46',
                                 font=('thesans', 19))
        self.reminder.pack(pady=5)

        self.db = database_connection()

    def handle_login(self):
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
                messagebox.showerror("Login", "Invalid Username or Password")

        except Error as e:
            messagebox.showerror("Error", "Error, Please connect to the internet")
            print("Error while connecting to MySQL", e)

        finally:
            if self.db.is_connected():
                self.db.close()


# sidebar and header class
class Sidebar(ctk.CTkToplevel):
    def __init__(self, master, login_window):
        super().__init__(master)
        self.login_window = login_window
        self.geometry("600x400")
        self.title("نظام تقييم الاداء الالكتروني")
        self.rowconfigure((0, 2, 3, 4, 5, 6), weight=1)
        self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.config(bg='#fff')

        self.menu_icon = tk.PhotoImage(file='icons/menu.png')
        self.close_icon = tk.PhotoImage(file='icons/close.png')

        # Header
        header = tk.Frame(self, bg="#141E46", highlightthickness=3)
        header.grid(row=0, column=0, sticky='nwe', columnspan=8)

        self.menu_button = tk.Button(header, bd=0, image=self.menu_icon, activebackground="#141E46", fg='white',
                                     bg='#141E46', font=('thesans', 20), command=self.menu_toggle)
        self.menu_button.grid(row=0, column=0, sticky='we')

        header_label = tk.Label(header, bg="#141E46", fg='#41B06E', text="نظام تقييم الاداء الالكتروني",
                                font=('thesans', 22))
        header_label.place(rely=0.5, relx=0.5, anchor='center')

        # Menu items
        self.menu_item_frame = tk.Frame(self, bg="#141E46", highlightthickness=5, height=100)

        # result_btn = tk.Button(self.menu_item_frame, text='النتيجة النهائية')
        exit_btn = tk.Button(self.menu_item_frame, text='اغلاق التطبيق', command=exit)
        logout_btn = tk.Button(self.menu_item_frame, text='تسجيل الخروج', command=self.logout)
        about_btn = tk.Button(self.menu_item_frame, text='عن البرنامج', command=self.about)
        help_btn = tk.Button(self.menu_item_frame, text='المساعدة', command=self.help)

        # المعلومات التي تظهر في الشاشة الرئيسية
        self.info_frame = tk.Frame(self, width=500, height=500, bg='#fff', bd=0)
        self.info_frame.grid(row=1, column=3, sticky='we')

        self.db = database_connection()

        username = self.login_window.username_entry.get()
        self.cursor = self.db.cursor()
        self.cursor.execute("SELECT id, fullname, college, department, created_at FROM users WHERE username=%s",
                            (username,))
        user_info = self.cursor.fetchone()

        id = user_info[0]
        fullname = user_info[1]
        message = f'مرحبا بك {fullname}'
        college = user_info[2]
        department = user_info[3]
        created_at = user_info[4].strftime('%d-%m-%Y')

        # userinfo_label = tk.Label(self.info_frame, text=f'{user_info}', font=('thesans', 18), fg='#141E46')
        # userinfo_label.grid(row=2, column=0, sticky='news')

        # username = self.login_window.username_entry.get().capitalize()
        message_label = tk.Label(self.info_frame, text=message, font=('thesans', 20), fg='#FF6600')
        message_label.grid(row=0, column=0, sticky='news')

        college_label = tk.Label(self.info_frame, text=f'{college} :الكلية', font=('thesans', 18), fg='#141E46')
        college_label.grid(row=2, column=0, sticky='news')

        department_label = tk.Label(self.info_frame, text=f'{department} :القسم', font=('thesans', 18), fg='#141E46')
        department_label.grid(row=3, column=0, sticky='news')

        # created_at_label = tk.Label(self.info_frame, text=f'تاريخ التسجيل: {created_at}', font=('thesans', 18), fg='#141E46')
        # created_at_label.grid(row=4, column=0, sticky='news')

        # id_label = tk.Label(self.info_frame, text=f'رقم الهوية: {id}', font=('thesans', 18), fg='#141E46')
        # id_label.grid(row=5, column=0, sticky='news')

        next_btn = tk.Button(self.info_frame, text='المحور الاول', font=('thesans', 18), fg='#FF6600',
                             command=self.changeToSide)
        next_btn.grid(row=6, column=0, sticky='news')

        # final_result_btn = tk.Button(self.info_frame, text='النتيجة النهائية', font=('thesans', 18), fg='#FF6600', command=self.changeToFinaResult)
        # final_result_btn.grid(row=7, column=0, sticky='news')

        for wed in self.info_frame.winfo_children():
            wed.configure(bg='#fff', fg='#141E46')

        for widget in self.menu_item_frame.winfo_children():
            widget.grid_configure(padx=10, pady=2)
            widget.configure(bd=0, font=('thesans', 16), fg='#41B06E', bg='#141E46')

    def changeToSide(self):
        self.withdraw()
        first_side_window = FirstSidewindow(self.master, self.login_window)


    # def changeToFinaResult(self):
    #     self.withdraw()
    #     final_result_window = FinalResult(self.master, self.login_window)
    #     final_result_window.deiconify()

    def logout(self):
        self.destroy()
        self.login_window.master.deiconify()

    def exit(self):
        self.quit()

    def about(self):
        messagebox.showinfo('حول', 'نظام تقييم الاداء الالكتروني\n كلية علوم الحاسوب والرياضيات\n الاصدار 1.0')

    def help(self):
        messagebox.showinfo('المساعدة',
                            'طريقة استخدام النظام والتقديم اولا يجب ملئ جميع المحاور ومن ثم الحصول على نتيجة التقييم وبعدها لايمكن التقديم مرة اخرى الا بعد سنة وحسب الموعد المقرر من قبل الكلية ')

    def menu_toggle(self):
        if self.menu_button.cget('image') == str(self.menu_icon):
            self.menu_button.config(image=self.close_icon)
            self.menu_item_frame.grid(row=0, column=0, sticky='wsn', rowspan=6, pady=80)
            self.info_frame.grid_forget()

        elif self.menu_button.cget('image') == str(self.close_icon):
            self.info_frame.grid(row=1, column=3, sticky='we')
            self.menu_button.config(image=self.menu_icon)
            self.menu_item_frame.grid_forget()


####laith####
class FirstSidewindow(ctk.CTkToplevel):
    def __init__(self, master, login_window):
        super().__init__(master)
        self.login_window = login_window
        self.geometry("900x700+350+30")
        self.title(" المحور الاول")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.config(bg='#DDF2FD')

        # lab1 = tk.Label(self, text="المحور الاول")
        # lab1.pack()

        # btback = tk.Button(self, text="الرجوع الى قائمة الرئيسية ",command=self.back)
        # btback.pack()

        # btback2 = tk.Button(self, text=" تكملة المحور الاول",command=self.go2)
        # btback2.place(x=50, y=650)

        lab1 = tk.Label(self, text=" المحور الاول :التدريس (40%) يملى من قبل اللجنة العلمية",
                        font=("thesans", 20, "bold"))
        lab1.place(x=270, y=20)

        lab2 = tk.Label(self,
                        text="عددالمقررات التي قام بتدريسها تمنح10د لكل مقرر دراسي (اولية او عليا) (نظري او عملي)",
                        font=("thesans", 16, "bold"))
        lab2.place(x=470, y=100)

        lab3 = tk.Label(self, text="10د/مقرر سنويالدراسات الاولية", font=("thesans", 16))
        lab3.place(x=890, y=150)

        self.one_lab3var = tk.BooleanVar()
        lab3check = tk.Checkbutton(self, variable=self.one_lab3var)
        lab3check.place(x=850, y=150)

        lab4 = tk.Label(self, text="الدراسات العليا", font=("thesans", 16))
        lab4.place(x=730, y=150)

        self.one_lab4var = tk.BooleanVar()
        lab4check = tk.Checkbutton(self, variable=self.one_lab4var)
        lab4check.place(x=690, y=150)

        lab5 = tk.Label(self, text="5د/مقرر فصليالدراسات الاولية", font=("thesans", 16))
        lab5.place(x=890, y=200)

        self.one_lab5var = tk.BooleanVar()
        lab5check = tk.Checkbutton(self, variable=self.one_lab5var)
        lab5check.place(x=850, y=200)

        lab6 = tk.Label(self, text="الدراسات العليا", font=("thesans", 16))
        lab6.place(x=730, y=200)

        self.one_lab6var = tk.BooleanVar()
        lab6check = tk.Checkbutton(self, variable=self.one_lab6var)
        lab6check.place(x=690, y=200)

        lab7 = tk.Label(self, text="للتدريسي الاداريوالمتفرغين جزئيا لاغراض الدراسة", font=("thesans", 16, "bold"))
        lab7.place(x=755, y=250)

        lab8 = tk.Label(self, text="20د/مقرر سنويالدراسات الاولية", font=("thesans", 16))
        lab8.place(x=890, y=300)

        self.one_lab8var = tk.BooleanVar()
        lab8check = tk.Checkbutton(self, variable=self.one_lab8var)
        lab8check.place(x=850, y=300)

        lab9 = tk.Label(self, text="الدراسات العليا", font=("thesans", 16))
        lab9.place(x=730, y=300)

        self.one_lab9var = tk.BooleanVar()
        lab9check = tk.Checkbutton(self, variable=self.one_lab9var)
        lab9check.place(x=690, y=300)

        lab10 = tk.Label(self, text="10د/مقرر فصليالدراسات الاولية", font=("thesans", 16))
        lab10.place(x=890, y=350)

        self.one_lab10var = tk.BooleanVar()
        lab10check = tk.Checkbutton(self, variable=self.one_lab10var)
        lab10check.place(x=850, y=350)

        lab11 = tk.Label(self, text="الدراسات العليا", font=("thesans", 16))
        lab11.place(x=730, y=350)

        self.one_lab11var = tk.BooleanVar()
        lab11check = tk.Checkbutton(self, variable=self.one_lab11var)
        lab11check.place(x=690, y=350)

        lab12 = tk.Label(self,
                         text="يعتمد كل (2) نشاط (رياضي , فني, كشفي, ثقافي ) مادة دراسية واحدةلتدريسي النشاطات الطلابية",
                         font=("thesans", 16), bg="red")
        lab12.place(x=470, y=400)

        lab13 = tk.Label(self,
                         text="ادارة الصف والعلاقة مع الطلبة واثارة دافعيتهممن خلال نسبة الاستبيان تمنح الدرجة كالاتي",
                         font=("thesans", 16))
        lab13.place(x=510, y=450)

        lab14 = tk.Label(self, text="(20د):80%فأكثر(16د):70-79%(12د):60-69%(8د):50-59%(4د):دون ذلك", font=("thesans", 16))
        lab14.place(x=510, y=500)

        self.one_lab14var = tk.IntVar()
        lab14combo = ttk.Combobox(self, values=[50, 60, 70, 80], textvariable=self.one_lab14var)
        lab14combo.place(x=350, y=505)

        lab15 = tk.Label(self,
                         text="التعليم المدمج:طرائق التدريسوالوسائل الحديثة في ايصال المعلومات والمعارف والمهارات من منصات الكترونية ما هي",
                         font=("thesans", 16), bg="red")
        lab15.place(x=340, y=550)

        lab16 = tk.Label(self,
                         text="يستخدم طرائق تدريس متعددة (المحاضرة ، المناقشة ، الاستقصاء ، العصف الذهني ، غيرها)",
                         font=("thesans", 16))
        lab16.place(x=500, y=600)

        self.one_lab16var = tk.BooleanVar()
        lab16chek = tk.Checkbutton(self, variable=self.one_lab16var)
        lab16chek.place(x=450, y=600)

        lab17 = tk.Label(self, text="يستخدم الامثلة التوضيحية والتطبيقية لأثراء المادة التعليمية", font=("thesans", 16))
        lab17.place(x=730, y=650)

        self.one_lab17var = tk.BooleanVar()
        lab17chek = tk.Checkbutton(self, variable=self.one_lab17var)
        lab17chek.place(x=700, y=650)

        lab18 = tk.Label(self, text="يستخدم وسائل الإيضاح او عرض افلام علمية متخصصة او اي وسيلة اخرى.",
                         font=("thesans", 16))
        lab18.place(x=600, y=700)

        self.one_lab18var = tk.BooleanVar()
        lab18chek = tk.Checkbutton(self, variable=self.one_lab18var)
        lab18chek.place(x=550, y=700)

        lab19 = tk.Label(self, text="ينشر محاضراته وفعالياته العلمية على الموقع الالكتروني (على ان لا تقل عن10محاضرات)",
                         font=("thesans", 16))
        lab19.place(x=510, y=750)

        self.one_lab19var = tk.BooleanVar()
        lab19chek = tk.Checkbutton(self, variable=self.one_lab19var)
        lab19chek.place(x=470, y=750)

        lab20 = tk.Label(self, text="يستخدم المنصات الالكترونية للتواصل مع الطلبة مثلEdmodo, Moodle, Google Class room",
                         font=("thesans", 16))
        lab20.place(x=420, y=800)

        self.one_lab20var = tk.BooleanVar()
        lab20chek = tk.Checkbutton(self, variable=self.one_lab20var)
        lab20chek.place(x=370, y=800)

        lab21 = tk.Label(self, text="يستخدم الطرائق والوسائل الحديثةالمستخدمة في التعليم الالكتروني",
                         font=("thesans", 16))
        lab21.place(x=600, y=840)

        self.one_lab21var = tk.BooleanVar()
        lab21chek = tk.Checkbutton(self, variable=self.one_lab21var)
        lab21chek.place(x=550, y=840)

        Button_complate = tk.Button(self, text="gتكملة المحور الاول ", command=self.comp)
        Button_complate.place(x=300, y=300)

        calc_button = tk.Button(self, text="حساب النقاط")
        calc_button.place(x=50, y=650)

        self.score_label = tk.Label(self, text="النقاط: 0", font=("thesans", 20))
        self.score_label.place(x=200, y=650)

        def show_score():
            score = self.calculate_fisrt_side_score()
            self.score_label.config(text=f"النقاط: {score}", font=("thesans", 20))

        calc_button.config(command=show_score)

    def comp(self):
        self.withdraw()

        self.new_window = ctk.CTkToplevel(self)
        self.new_window.title("تكملة المحور الاول")

        self.new_window.geometry("900x700+350+30")
        self.new_window.title(" المحور الاول")
        self.new_window.rowconfigure(0, weight=1)
        self.new_window.columnconfigure(0, weight=1)
        self.new_window.config(bg='#DDF2FD')

        lab1 = tk.Label(self.new_window, text="الاساليب المستعملة في تقييم الطلبة", font=("thesans", 16, "bold"))
        lab1.place(x=850, y=30)

        lab2 = tk.Label(self.new_window,
                        text="يستخدم اساليب متنوعة لتقيم اداء الطلة مثل اختبارات تحريرية , شفوية ,ادائية , تقارير الكترونية ,انشطة الكترونيةو ",
                        font=("thesans", 16))
        lab2.place(x=330, y=100)

        self.new_window.one_lab22var = tk.BooleanVar()
        lab2chk = tk.Checkbutton(self.new_window, variable=self.new_window.one_lab22var)
        lab2chk.place(x=300, y=100)

        lab3 = tk.Label(self.new_window,
                        text=" يقوم بتقييم الطلبة بشكل دوري ومستمر وشامل طوال العام الدراسي ويعلن نتائج التقييم للطلبة في الوقت المناسب",
                        font=("thesans", 16))
        lab3.place(x=330, y=150)

        self.new_window.one_lab23var = tk.BooleanVar()
        lab3chk = tk.Checkbutton(self.new_window, variable=self.new_window.one_lab23var)
        lab3chk.place(x=300, y=150)

        lab4 = tk.Label(self.new_window,
                        text=" يقدم تغذية راجعة للطلبة حول ادائهم في الاختبارات ويعرض الاجوبة النموذجية لاسئلة الاختبارات الدورية",
                        font=("thesans", 16))
        lab4.place(x=330, y=200)

        self.new_window.one_lab24var = tk.BooleanVar()
        lab4chk = tk.Checkbutton(self.new_window, variable=self.new_window.one_lab24var)
        lab4chk.place(x=300, y=200)

        lab5 = tk.Label(self.new_window, text="وصف المقرر الدراسي وتحديثه-موجود:", font=("thesans", 16, "bold"))
        lab5.place(x=800, y=250)

        lab6 = tk.Label(self.new_window, text=" يقدم وصف المقرر الدراسي في بداية العام الدراسي", font=("thesans", 16))
        lab6.place(x=330, y=300)

        self.new_window.one_lab26var = tk.BooleanVar()
        lab6chk = tk.Checkbutton(self.new_window, variable=self.new_window.one_lab26var)
        lab6chk.place(x=300, y=300)

        lab7 = tk.Label(self.new_window, text="يعرض مفردات المقرر ويوزع الانشطة والواجبات على الطلبة",
                        font=("thesans", 16))
        lab7.place(x=330, y=350)

        self.new_window.one_lab27var = tk.BooleanVar()
        lab7chk = tk.Checkbutton(self.new_window, variable=self.new_window.one_lab27var)
        lab7chk.place(x=300, y=350)

        lab8 = tk.Label(self.new_window,
                        text="يقدم مقترحات لتطوير المقرر ومفرداته ويستخدم المصادر الحديثة في اعداد المحاضرات والانشطة دوريا",
                        font=("thesans", 16))
        lab8.place(x=330, y=400)

        self.new_window.one_lab28var = tk.BooleanVar()
        lab8chk = tk.Checkbutton(self.new_window, variable=self.new_window.one_lab28var)
        lab8chk.place(x=300, y=400)

        btgo = tk.Button(self.new_window, text=" المحور الثاني   ", command=self.go2)
        btgo.place(x=850, y=650)

    def back(self):
        self.destroy()
        self.login_window.master.withdraw()
        self.login_window.master.deiconify()

    def go2(self):
        self.destroy()
        self.second_sidewindow = SecondSidewindow(self.master, self.login_window)
        self.second_sidewindow.deiconify()

    def calculate_fisrt_side_score(self):
        score = 0

        # تقييم المقررات الدراسية
        if self.one_lab3var.get():
            score += 10
        if self.one_lab4var.get():
            score += 10
        if self.one_lab5var.get():
            score += 5
        if self.one_lab6var.get():
            score += 5
        if self.one_lab8var.get():
            score += 20
        if self.one_lab9var.get():
            score += 20
        if self.one_lab10var.get():
            score += 10
        if self.one_lab11var.get():
            score += 10

        # إدارة الصف والعلاقة مع الطلبة
        selected_percentage = self.one_lab14var.get()
        if selected_percentage >= 80:
            score += 20
        elif 70 <= selected_percentage < 80:
            score += 16
        elif 60 <= selected_percentage < 70:
            score += 12
        elif 50 <= selected_percentage < 60:
            score += 8
        else:
            score += 4

        # الأساليب المستعملة في تقييم الطلبة
        if self.one_lab16var.get():
            score += 5
        if self.one_lab17var.get():
            score += 5
        if self.one_lab18var.get():
            score += 5
        if self.one_lab19var.get():
            score += 5
        if self.one_lab20var.get():
            score += 5
        if self.one_lab21var.get():
            score += 5
        if hasattr(self, 'new_window'):
            if self.new_window.one_lab22var.get():
                score += 5
            if self.new_window.one_lab23var.get():
                score += 5
            if self.new_window.one_lab24var.get():
                score += 5
            if self.new_window.one_lab26var.get():
                score += 5
            if self.new_window.one_lab27var.get():
                score += 5
            if self.new_window.one_lab28var.get():
                score += 5

        return score


class SecondSidewindow(ctk.CTkToplevel):
    def __init__(self, master, login_window):
        super().__init__(master)
        self.login_window = login_window
        self.geometry("900x700+350+30")
        self.title(" المحور الثاني")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.config(bg='#DDF2FD')

        btgo = tk.Button(self, text="تكملة المحور الثاني", command=self.comp2)
        btgo.place(x=50, y=100)

        lab1 = tk.Label(self,
                        text="المحور الثاني:النشاط العلمي والبحثي (40% ) يملئ من قبلاللجنة العلمية بعد ان تقدم الوثائق منقبل صاحب العلاقة",
                        font=("thesans", 20, "bold"))
        lab1.place(x=100, y=30)

        lab2 = tk.Label(self, text="عددالبحوث المنشورة", font=("thesans", 16))
        lab2.place(x=900, y=90)

        lab3 = tk.Label(self, text="عالمي سكوبس-معامل التاثير ", font=("thesans", 16))
        lab3.place(x=800, y=130)

        self.lab3var = tk.IntVar()
        lab3chk = tk.Entry(self, textvariable=self.lab3var)
        lab3chk.place(x=650, y=130)

        lab4 = tk.Label(self, text="  عالمي كلارفيك معلمب التاثير ", font=("thesans", 16))
        lab4.place(x=720, y=170)

        self.lab4var = tk.IntVar()
        lab4chk = tk.Entry(self, textvariable=self.lab4var)
        lab4chk.place(x=600, y=170)

        lab5 = tk.Label(self, text="عالمي او عربي او محلي على ان لا تكون مفترسة", font=("thesans", 16))
        lab5.place(x=700, y=220)

        self.lab5var = tk.BooleanVar()
        lab5chk = tk.Checkbutton(self, variable=self.lab5var)
        lab5chk.place(x=660, y=220)

        lab6 = tk.Label(self, text="تقويم البحوث والمقالات العلمية والرسائل والاطاريح وبرائات الاختراع ",
                        font=("thesans", 16))
        lab6.place(x=630, y=270)
        self.lab6var = tk.BooleanVar()
        lab6chk = tk.Checkbutton(self, variable=self.lab6var)
        lab6chk.place(x=600, y=270)

        lab7 = tk.Label(self,
                        text="كتاب المولف العلميي او المنهجي او المترجم شرط ان يكون مقوم علميااو المنشور في دار النشر العالمية",
                        font=("thesans", 16))
        lab7.place(x=430, y=300)
        self.lab7var = tk.BooleanVar()
        lab7chk = tk.Checkbutton(self, variable=self.lab7var)
        lab7chk.place(x=400, y=300)

        lab8 = tk.Label(self,
                        text="كتاب المولف العلمي او المنهجي او المترجم شرط ان يكون مقوم علميا ونشر في دار نشر عربية او محلية",
                        font=("thesans", 16))
        lab8.place(x=430, y=340)
        self.lab8var = tk.BooleanVar()
        lab8chk = tk.Checkbutton(self, variable=self.lab8var)
        lab8chk.place(x=400, y=340)

        lab9 = tk.Label(self, text="عددالاشراف", font=("thesans", 20, "bold"))
        lab9.place(x=100, y=100)

        lab10 = tk.Label(self, text="عشر درجات دكتوراه منفرد", font=("thesans", 16))
        lab10.place(x=100, y=140)

        self.lab10var = tk.BooleanVar()
        lab10chk = tk.Checkbutton(self, variable=self.lab10var)
        lab10chk.place(x=50, y=140)

        lab11 = tk.Label(self, text="خمسة درجات دكتوراه مشترك", font=("thesans", 16))
        lab11.place(x=100, y=180)
        self.lab11var = tk.BooleanVar()
        lab11chk = tk.Checkbutton(self, variable=self.lab11var)
        lab11chk.place(x=50, y=180)

        lab12 = tk.Label(self, text="ثمانية درجات ماجستير منفرد", font=("thesans", 16))
        lab12.place(x=100, y=220)
        self.lab12var = tk.BooleanVar()
        lab12chk = tk.Checkbutton(self, variable=self.lab12var)
        lab12chk.place(x=50, y=220)

        lab13 = tk.Label(self, text="اربعة درجات ماجستير مشترك", font=("thesans", 16))
        lab13.place(x=100, y=280)
        self.lab13var = tk.BooleanVar()
        lab13chk = tk.Checkbutton(self, variable=self.lab13var)
        lab13chk.place(x=50, y=280)

        lab14 = tk.Label(self, text="ستة درجات دبلوم عالي منفرد", font=("thesans", 16))
        lab14.place(x=100, y=320)
        self.lab14var = tk.BooleanVar()
        lab14chk = tk.Checkbutton(self, variable=self.lab14var)
        lab14chk.place(x=50, y=320)

        lab15 = tk.Label(self, text="ثلاثة درجات دبلوم عالي مشترك", font=("thesans", 16))
        lab15.place(x=100, y=380)
        self.lab15var = tk.BooleanVar()
        lab15chk = tk.Checkbutton(self, variable=self.lab15var)
        lab15chk.place(x=50, y=380)

        lab16 = tk.Label(self, text="اربعة درجات  بكالوريوس", font=("thesans", 16))
        lab16.place(x=100, y=420)
        self.lab16var = tk.BooleanVar()
        lab16chk = tk.Checkbutton(self, variable=self.lab16var)
        lab16chk.place(x=50, y=420)

        lab17 = tk.Label(self, text="المشاركة في الموتمارات \n العلمية", font=("thesans", 16))
        lab17.place(x=900, y=500)

        lab18 = tk.Label(self, text="الندوات", font=("thesans", 16))
        lab18.place(x=900, y=580)

        lab19 = tk.Label(self, text="الدورات التدريبية", font=("thesans", 16))
        lab19.place(x=900, y=660)

        lab20 = tk.Label(self, text="ورش عمل", font=("thesans", 16))
        lab20.place(x=900, y=720)

        lab21 = tk.Label(self, text="عدد كمحاضر", font=("thesans", 16))
        lab21.place(x=750, y=450)

        lab22 = tk.Label(self, text="دولي عالمي\nخارج العراق", font=("thesans", 16))
        lab22.place(x=630, y=450)

        lab23 = tk.Label(self, text="داخل العراق", font=("thesans", 16))
        lab23.place(x=520, y=450)

        lab24 = tk.Label(self, text="عدد كحضور", font=("thesans", 16))
        lab24.place(x=420, y=450)

        lab25 = tk.Label(self, text="دولي عالمي\nخارج العراق", font=("thesans", 16))
        lab25.place(x=330, y=450)

        lab26 = tk.Label(self, text="داخل العراق", font=("thesans", 16))
        lab26.place(x=220, y=470)

        lab27 = tk.Label(self, text="الموتمرات العلمية \nبحث منفرد", font=("thesans", 16))
        lab27.place(x=750, y=500)

        lab28 = tk.Label(self, text="الموتمرات العلمية \nبحث مشترك", font=("thesans", 16))
        lab28.place(x=750, y=570)

        lab29 = tk.Label(self, text="الموتمرات العلمية بوستر ", font=("thesans", 16))
        lab29.place(x=700, y=650)

        lab30 = tk.Label(self, text="الندوات", font=("thesans", 16))
        lab30.place(x=700, y=700)

        lab31 = tk.Label(self, text="الدورات التدريبية", font=("thesans", 16))
        lab31.place(x=700, y=730)

        lab32 = tk.Label(self, text="ورش عمل", font=("thesans", 16))
        lab32.place(x=700, y=770)

        lab33 = tk.Label(self, text="الموتمرات العلمية", font=("thesans", 16))
        lab33.place(x=420, y=520)

        lab34 = tk.Label(self, text="الندوات", font=("thesans", 16))
        lab34.place(x=420, y=600)

        lab35 = tk.Label(self, text="الدورات التدريبية", font=("thesans", 16))
        lab35.place(x=420, y=670)

        lab36 = tk.Label(self, text="ورش العمل", font=("thesans", 16))
        lab36.place(x=420, y=750)

        # موتمرات علمية دولي عالمي خارج العرق بحث منفرد
        self.lab17var = tk.BooleanVar()
        lab17chk = tk.Checkbutton(self, variable=self.lab17var)
        lab17chk.place(x=650, y=520)

        # داخل العراق
        self.lab18var = tk.BooleanVar()
        lab18chk = tk.Checkbutton(self, variable=self.lab18var)
        lab18chk.place(x=550, y=520)

        # عدد حضور مةتمرات علمية دولي عالمي
        self.lab19var = tk.IntVar()
        lab19chk = tk.Checkbutton(self, variable=self.lab19var)
        lab19chk.place(x=350, y=520)

        # داخل العراق
        self.lab20var = tk.IntVar()
        lab20chk = tk.Checkbutton(self, variable=self.lab20var)
        lab20chk.place(x=230, y=520)

        # محاضر موتمرات علمية بحث مشترك دولي عالمي خارجالعراق
        self.lab21var = tk.BooleanVar()
        lab21chk = tk.Checkbutton(self, variable=self.lab21var)
        lab21chk.place(x=650, y=600)

        # محاضر موتمرات علمية بحث مشترك   داخل العراق
        self.lab22var = tk.BooleanVar()
        lab22chk = tk.Checkbutton(self, variable=self.lab22var)
        lab22chk.place(x=550, y=600)

        # حضور ندوات دولي حارج العراق
        self.lab23var = tk.BooleanVar()
        lab23chk = tk.Checkbutton(self, variable=self.lab23var)
        lab23chk.place(x=350, y=600)

        # حضور ندوات دولي داخل العراق
        self.lab24var = tk.BooleanVar()
        lab23chk = tk.Checkbutton(self, variable=self.lab24var)
        lab23chk.place(x=230, y=600)

        # محاضر موتمرات علمية بوستر دولي خارج العراق
        self.lab25var = tk.BooleanVar()
        lab24chk = tk.Checkbutton(self, variable=self.lab25var)
        lab24chk.place(x=650, y=650)

        # محاضر موتمرات علمية بوستر  داخل العراق
        self.lab26var = tk.BooleanVar()
        lab25chk = tk.Checkbutton(self, variable=self.lab26var)
        lab25chk.place(x=550, y=650)

        # حضور دورات تدريبة خارج العراق
        self.lab27var = tk.BooleanVar()
        lab26chk = tk.Checkbutton(self, variable=self.lab27var)
        lab26chk.place(x=350, y=670)

        # حضور دورات تدريبة داخل العراق
        self.lab28var = tk.BooleanVar()
        lab27chk = tk.Checkbutton(self, variable=self.lab28var)
        lab27chk.place(x=230, y=670)

        # محاضر ندوات دولي
        self.lab29var = tk.BooleanVar()
        lab28chk = tk.Checkbutton(self, variable=self.lab29var)
        lab28chk.place(x=650, y=700)

        # محاضر ندوات داخل
        self.lab30var = tk.BooleanVar()
        lab29chk = tk.Checkbutton(self, variable=self.lab30var)
        lab29chk.place(x=550, y=700)

        # محاضر دورات تدريبية دولي
        self.lab31var = tk.BooleanVar()
        lab30chk = tk.Checkbutton(self, variable=self.lab31var)
        lab30chk.place(x=650, y=730)

        # محاضر دورات تدريبية داخل
        self.lab32var = tk.BooleanVar()
        lab31chk = tk.Checkbutton(self, variable=self.lab32var)
        lab31chk.place(x=550, y=730)

        # محاضر ورش عمل دولي
        self.lab33var = tk.BooleanVar()
        lab32chk = tk.Checkbutton(self, variable=self.lab33var)
        lab32chk.place(x=650, y=760)

        # محاضر ورش عمل داخل
        self.lab34var = tk.BooleanVar()
        lab33chk = tk.Checkbutton(self, variable=self.lab34var)
        lab33chk.place(x=550, y=760)

        # حضور ورش عمل حارج دولي عالمي
        self.lab35var = tk.BooleanVar()
        lab34chk = tk.Checkbutton(self, variable=self.lab35var)
        lab34chk.place(x=350, y=760)

        # حضور ورش عمل حارج دولي عالمي
        self.lab35var = tk.BooleanVar()
        lab35chk = tk.Checkbutton(self, variable=self.lab35var)
        lab35chk.place(x=230, y=760)

        calc_button = tk.Button(self, text="حساب النقاط")
        calc_button.place(x=50, y=650)

        self.score_label = tk.Label(self, text="النقاط: 0", font=("thesans", 20))
        self.score_label.place(x=200, y=650)

        def show_score():
            score = self.calculate_second_side_score()
            self.score_label.config(text=f"النقاط: {score}")

        calc_button.config(command=show_score)

    def comp2(self):
        self.withdraw()

        self.new_window2 = ctk.CTkToplevel(self)
        self.new_window2.title("تكملة المحور الثاني")
        self.new_window2.geometry("900x700+350+30")
        self.new_window2.title("تكملة المحور الثاني")
        self.new_window2.rowconfigure(0, weight=1)
        self.new_window2.columnconfigure(0, weight=1)
        self.new_window2.config(bg='#DDF2FD')

        btgo = tk.Button(self.new_window2, text=" المحور الثالث   ", command=self.go2)
        btgo.place(x=50, y=50)
        lab1 = tk.Label(self.new_window2, text="المساهمة في خدمة الموسسات العلمية خارج وزارة التعليم",
                        font=("thesans", 20, "bold"))
        lab1.place(x=600, y=20)

        lab2 = tk.Label(self.new_window2, text="خدمة او استشارة", font=("thesans", 16))
        lab2.place(x=1000, y=70)

        self.new_window2.lab36var = tk.BooleanVar()
        lab2chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab36var)
        lab2chk.place(x=950, y=70)

        lab3 = tk.Label(self.new_window2, text="اقامة ندوة ", font=("arial", 16))
        lab3.place(x=1000, y=120)
        self.new_window2.lab37var = tk.BooleanVar()
        lab3chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab37var)
        lab3chk.place(x=950, y=120)

        lab4 = tk.Label(self.new_window2, text=" ملتقى ثقافي او علمي ", font=("arial", 16))
        lab4.place(x=950, y=170)
        self.new_window2.lab38var = tk.BooleanVar()
        lab4chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab38var)
        lab4chk.place(x=900, y=170)

        lab5 = tk.Label(self.new_window2, text="ورشة عمل", font=("arial", 16))
        lab5.place(x=1000, y=220)
        self.new_window2.lab39var = tk.BooleanVar()
        lab5chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab39var)
        lab5chk.place(x=950, y=220)

        lab6 = tk.Label(self.new_window2, text="محاضرة", font=("arial", 16))
        lab6.place(x=800, y=70)
        self.new_window2.lab40var = tk.BooleanVar()
        lab6chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab40var)
        lab6chk.place(x=750, y=70)

        lab7 = tk.Label(self.new_window2, text="دورة تدريبية", font=("arial", 16))
        lab7.place(x=800, y=120)
        self.new_window2.lab41var = tk.BooleanVar()
        lab7chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab41var)
        lab7chk.place(x=750, y=120)

        lab8 = tk.Label(self.new_window2, text="لقاء صحفي", font=("arial", 16))
        lab8.place(x=800, y=170)
        self.new_window2.lab42var = tk.BooleanVar()
        lab8chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab42var)
        lab8chk.place(x=750, y=170)

        lab9 = tk.Label(self.new_window2, text="نشر مقالة في مجلة", font=("arial", 16))
        lab9.place(x=800, y=220)
        self.new_window2.lab43var = tk.BooleanVar()
        lab9chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab43var)
        lab9chk.place(x=750, y=220)

        lab10 = tk.Label(self.new_window2, text="زيارة دار الايتام والمسنين", font=("arial", 16))
        lab10.place(x=500, y=70)
        self.new_window2.lab44var = tk.BooleanVar()
        lab10chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab44var)
        lab10chk.place(x=450, y=70)

        lab11 = tk.Label(self.new_window2, text="خدمة المستشفيات التعليمية", font=("arial", 16))
        lab11.place(x=500, y=120)
        self.new_window2.lab45var = tk.BooleanVar()
        lab11chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab45var)
        lab11chk.place(x=450, y=120)

        lab12 = tk.Label(self.new_window2, text="خدمةالمؤسسات الخدميةاوالانتاجية الحكومية", font=("arial", 16))
        lab12.place(x=450, y=170)
        self.new_window2.lab46var = tk.BooleanVar()
        lab12chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab46var)
        lab12chk.place(x=400, y=170)

        lab13 = tk.Label(self.new_window2, text="اخرى:", font=("arial", 16))
        lab13.place(x=450, y=220)
        self.new_window2.lab47var = tk.BooleanVar()
        lab13chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab47var)
        lab13chk.place(x=400, y=220)

        lab14 = tk.Label(self.new_window2, text="المشاركة في التعليم المستمر والحلقات العلمية والثقافية والسنمار",
                         font=("arial", 20, "bold"))
        lab14.place(x=530, y=280)

        lab15 = tk.Label(self.new_window2, text="محاضر في التعليم المستمر", font=("arial", 16))
        lab15.place(x=900, y=340)

        self.new_window2.lab48var = tk.BooleanVar()
        lab15chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab48var)
        lab15chk.place(x=850, y=340)

        lab16 = tk.Label(self.new_window2, text="دورات طرائق التدريسالحديثةفي التعليم المستمر", font=("arial", 16))
        lab16.place(x=800, y=380)
        self.new_window2.lab49var = tk.BooleanVar()
        lab16chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab49var)
        lab16chk.place(x=750, y=380)

        lab17 = tk.Label(self.new_window2, text="حضوردورة تعليم مستمر", font=("arial", 16))
        lab17.place(x=600, y=340)
        self.new_window2.lab50var = tk.BooleanVar()
        lab17chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab50var)
        lab17chk.place(x=550, y=340)

        lab18 = tk.Label(self.new_window2, text="عضو لجنة الحلقات الثقافية والسمنار", font=("arial", 16))
        lab18.place(x=500, y=380)
        self.new_window2.lab51var = tk.BooleanVar()
        lab18chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab51var)
        lab18chk.place(x=450, y=380)

        lab19 = tk.Label(self.new_window2,
                         text="المشاركة في الزيارات الميدانية او الحقلية او اجراء اختبارات  او تحليلات معملية او مختبرية",
                         font=("arial", 20, "bold"))
        lab19.place(x=300, y=420)

        lab20 = tk.Label(self.new_window2, text="الزيارات الميدانية للاشراف على الطلبة ضمن الاختصاص",
                         font=("arial", 16))
        lab20.place(x=700, y=480)
        self.new_window2.lab52var = tk.BooleanVar()
        lab20chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab52var)
        lab20chk.place(x=650, y=480)

        lab21 = tk.Label(self.new_window2, text="الزيارات الحقلية", font=("arial", 16))
        lab21.place(x=700, y=520)
        self.new_window2.lab53var = tk.BooleanVar()
        lab21chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab53var)
        lab21chk.place(x=650, y=520)

        lab22 = tk.Label(self.new_window2, text="اجراء اختبارات", font=("arial", 16))
        lab22.place(x=700, y=560)
        self.new_window2.lab54var = tk.BooleanVar()
        lab22chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab54var)
        lab22chk.place(x=650, y=560)

        lab23 = tk.Label(self.new_window2, text="تحليلات معملي", font=("arial", 16))
        lab23.place(x=700, y=600)
        self.new_window2.lab55var = tk.BooleanVar()
        lab23chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab55var)
        lab23chk.place(x=650, y=600)

        lab24 = tk.Label(self.new_window2, text="تحليلات مختبرية", font=("arial", 16))
        lab24.place(x=700, y=640)
        self.new_window2.lab56var = tk.BooleanVar()
        lab24chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab56var)
        lab24chk.place(x=650, y=640)

        lab25 = tk.Label(self.new_window2, text="الزيارات والسفرات العلمية", font=("arial", 16))
        lab25.place(x=700, y=680)
        self.new_window2.lab57var = tk.BooleanVar()
        lab25chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab57var)
        lab25chk.place(x=650, y=680)

        lab26 = tk.Label(self.new_window2, text="اخرى :", font=("arial", 16))
        lab26.place(x=700, y=720)
        self.new_window2.lab58var = tk.BooleanVar()
        lab26chk = tk.Checkbutton(self.new_window2, variable=self.new_window2.lab58var)
        lab26chk.place(x=650, y=720)

    def go2(self):
        self.destroy()
        self.second_sidewindow = TherdSidewindow(self.master, self.login_window)
        self.second_sidewindow.deiconify()

    def calculate_second_side_score(self):
        score = 0
        if self.lab3var.get():
            score += 10
        if self.lab4var.get():
            score += 10
        if self.lab5var.get():
            score += 10
        if self.lab6var.get():
            score += 10
        if self.lab7var.get():
            score += 10
        if self.lab8var.get():
            score += 10
        if self.lab10var.get():
            score += 10
        if self.lab11var.get():
            score += 10
        if self.lab12var.get():
            score += 10
        if self.lab13var.get():
            score += 10
        if self.lab14var.get():
            score += 10
        if self.lab15var.get():
            score += 10
        if self.lab16var.get():
            score += 10
        if self.lab17var.get():
            score += 10
        if self.lab18var.get():
            score += 10
        if self.lab19var.get():
            score += 10
        if self.lab20var.get():
            score += 10
        if self.lab21var.get():
            score += 10
        if self.lab22var.get():
            score += 10
        if self.lab23var.get():
            score += 10
        if self.lab24var.get():
            score += 10
        if self.lab25var.get():
            score += 10
        if self.lab26var.get():
            score += 10
        if self.lab27var.get():
            score += 10
        if self.lab28var.get():
            score += 10
        if self.lab29var.get():
            score += 10
        if self.lab30var.get():
            score += 10
        if self.lab31var.get():
            score += 10
        if self.lab32var.get():
            score += 10
        if self.lab33var.get():
            score += 10
        if self.lab34var.get():
            score += 10
        if self.lab35var.get():
            score += 10

        #تكملة المحور الثاني
        if hasattr(self, 'new_window2'):
            if self.new_window2.lab36var.get():
                score += 10
            if self.new_window2.lab37var.get():
                score += 10
            if self.new_window2.lab38var.get():
                score += 10
            if self.new_window2.lab39var.get():
                score += 10
            if self.new_window2.lab40var.get():
                score += 10
            if self.new_window2.lab41var.get():
                score += 10
            if self.new_window2.lab42var.get():
                score += 10
            if self.new_window2.lab43var.get():
                score += 10
            if self.new_window2.lab44var.get():
                score += 10
            if self.new_window2.lab45var.get():
                score += 10
            if self.new_window2.lab46var.get():
                score += 10
            if self.new_window2.lab47var.get():
                score += 10
            if self.new_window2.lab48var.get():
                score += 10
            if self.new_window2.lab49var.get():
                score += 10
            if self.new_window2.lab50var.get():
                score += 10
            if self.new_window2.lab51var.get():
                score += 10
            if self.new_window2.lab52var.get():
                score += 10
            if self.new_window2.lab53var.get():
                score += 10
            if self.new_window2.lab54var.get():
                score += 10
            if self.new_window2.lab55var.get():
                score += 10
            if self.new_window2.lab56var.get():
                score += 10
            if self.new_window2.lab57var.get():
                score += 10
            if self.new_window2.lab58var.get():
                score += 10
        return score


class TherdSidewindow(ctk.CTkToplevel):
    def __init__(self, master, login_window):
        super().__init__(master)
        self.login_window = login_window
        self.geometry("900x700+350+30")
        self.title(" المحور الثالث")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.config(bg='#DDF2FD')

        btgo = tk.Button(self, text=" المحور الرابع   ", command=self.go2)
        btgo.pack()

        lab1 = tk.Label(self, text="الجانب التربوي والتكليفات الاخرى", font=("arial", 20, "bold"))
        lab1.place(x=800, y=20)

        lab2 = tk.Label(self, text="المساهمة في خدمة الموسسات العلمية خارج وزارة التعليم", font=("arial", 20, "bold"))
        lab2.place(x=600, y=80)

        lab3 = tk.Label(self, text="عضو لجنة امتحانية", font=("arial", 16))
        lab3.place(x=950, y=120)
        self.lab3var = tk.BooleanVar()
        lab3chk = tk.Checkbutton(self, variable=self.lab3var)
        lab3chk.place(x=900, y=120)

        lab4 = tk.Label(self, text="عضو لجنة دائمية", font=("arial", 16))
        lab4.place(x=750, y=120)
        self.lab4var = tk.BooleanVar()
        lab4chk = tk.Checkbutton(self, variable=self.lab4var)
        lab4chk.place(x=700, y=120)

        lab5 = tk.Label(self, text="عضو لجنة موقتة", font=("arial", 16))
        lab5.place(x=550, y=120)
        self.lab5var = tk.BooleanVar()
        lab5chk = tk.Checkbutton(self, variable=self.lab5var)
        lab5chk.place(x=500, y=120)

        lab6 = tk.Label(self, text="الالتزام الوظيفي", font=("arial", 16))
        lab6.place(x=950, y=180)
        self.lab6var = tk.BooleanVar()
        lab6chk = tk.Checkbutton(self, variable=self.lab6var)
        lab6chk.place(x=900, y=180)

        lab7 = tk.Label(self, text="اساليب التعامل مع الطلبة وتقديم المهارات الارشادية", font=("arial", 16))
        lab7.place(x=700, y=240)
        self.lab7var = tk.BooleanVar()
        lab7chk = tk.Checkbutton(self, variable=self.lab7var)
        lab7chk.place(x=650, y=240)

        lab8 = tk.Label(self, text="كتب الشكر والتقدير او الشهادة التقديرية خلال عام التقدير",
                        font=("arial", 20, "bold"))
        lab8.place(x=600, y=300)

        lab9 = tk.Label(self, text="وزيراو مايعادل درجته", font=("arial", 16))
        lab9.place(x=950, y=360)
        self.lab9var = tk.BooleanVar()
        lab9chk = tk.Checkbutton(self, variable=self.lab9var)
        lab9chk.place(x=900, y=360)

        lab10 = tk.Label(self, text="وكيل وزير اورئيس جامعة", font=("arial", 16))
        lab10.place(x=700, y=360)
        self.lab10var = tk.BooleanVar()
        lab10chk = tk.Checkbutton(self, variable=self.lab10var)
        lab10chk.place(x=650, y=360)

        lab11 = tk.Label(self, text="مساعد رئيس الجامعةاوعميد", font=("arial", 16))
        lab11.place(x=400, y=360)
        self.lab11var = tk.BooleanVar()
        lab11chk = tk.Checkbutton(self, variable=self.lab11var)
        lab11chk.place(x=350, y=360)

        lab12 = tk.Label(self, text="مشاركته في الاعمال التطوعية داخل الجامعة او خارجها", font=("arial", 20, "bold"))
        lab12.place(x=600, y=400)

        lab13 = tk.Label(self, text="حملات التشجير", font=("arial", 16))
        lab13.place(x=900, y=440)
        self.lab13var = tk.BooleanVar()
        lab13chk = tk.Checkbutton(self, variable=self.lab13var)
        lab13chk.place(x=850, y=440)

        lab14 = tk.Label(self, text="التبرع في ترميم وصبغ الابنية", font=("arial", 16))
        lab14.place(x=900, y=480)
        self.lab14var = tk.BooleanVar()
        lab14chk = tk.Checkbutton(self, variable=self.lab14var)
        lab14chk.place(x=850, y=480)

        lab15 = tk.Label(self, text="تصليح الاجهزة وصيانتها", font=("arial", 16))
        lab15.place(x=900, y=520)
        self.lab15var = tk.BooleanVar()
        lab15chk = tk.Checkbutton(self, variable=self.lab15var)
        lab15chk.place(x=850, y=520)

        lab16 = tk.Label(self, text="التبرع باجهزة متنوعة وبالكتب", font=("arial", 16))
        lab16.place(x=900, y=560)
        self.lab16var = tk.BooleanVar()
        lab16chk = tk.Checkbutton(self, variable=self.lab16var)
        lab16chk.place(x=850, y=560)

        lab17 = tk.Label(self, text="عمل البوسترات التوعوية", font=("thesans", 16))
        lab17.place(x=900, y=600)
        self.lab17var = tk.BooleanVar()
        lab17chk = tk.Checkbutton(self, variable=self.lab17var)
        lab17chk.place(x=850, y=600)

        lab18 = tk.Label(self, text="اخرى :", font=("arial", 16))
        lab18.place(x=900, y=640)
        self.lab18var = tk.BooleanVar()
        lab18chk = tk.Checkbutton(self, variable=self.lab18var)
        lab18chk.place(x=850, y=640)

        calc_button = tk.Button(self, text="حساب النقاط")
        calc_button.place(x=50, y=650)

        self.score_label = tk.Label(self, text="النقاط: 0", font=("thesans", 20))
        self.score_label.place(x=200, y=650)

        def show_score():
            score = self.calculate_third_side_score()
            self.score_label.config(text=f"النقاط: {score}", font=("thesans", 20))

        calc_button.config(command=show_score)

    def go2(self):
        self.destroy()
        self.second_sidewindow = ForthSidewindow(self.master, self.login_window)
        self.second_sidewindow.deiconify()

    def calculate_third_side_score(self):
        score = 0

        if self.lab3var.get():
            score += 10
        if self.lab4var.get():
            score += 10
        if self.lab5var.get():
            score += 10
        if self.lab6var.get():
            score += 10
        if self.lab7var.get():
            score += 10
        if self.lab9var.get():
            score += 10
        if self.lab10var.get():
            score += 10
        if self.lab11var.get():
            score += 10
        if self.lab13var.get():
            score += 10
        if self.lab14var.get():
            score += 10
        if self.lab15var.get():
            score += 10
        if self.lab16var.get():
            score += 10
        if self.lab17var.get():
            score += 10
        if self.lab18var.get():
            score += 10
        return score

class ForthSidewindow(ctk.CTkToplevel):
    def __init__(self, master, login_window):
        super().__init__(master)
        self.login_window = login_window
        self.geometry("900x700+350+30")
        self.title(" المحور الرابع")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.config(bg='#DDF2FD')

        lab1 = tk.Label(self, text="المحور الرابع :مواطن القوة", font=("thesans", 20, "bold"))
        lab1.place(x=850, y=30)

        lab2 = tk.Label(self, text="براءت اختراع  و الجوائز في عام التقييم حصرا ", font=("thesans", 16))
        lab2.place(x=800, y=80)
        self.lab2var = tk.BooleanVar()
        lab2chk = tk.Checkbutton(self, variable=self.lab2var)
        lab2chk.place(x=750, y=80)

        lab3 = tk.Label(self, text="امتلاك التدريسي لمعامل هيرش او سكور في بوابات البحث الحد الادنى 1",
                        font=("thesans", 16))
        lab3.place(x=620, y=120)

        self.lab3var = tk.IntVar()
        self.lab3var.set(1)
        lab3entry = tk.Entry(self, textvariable=self.lab3var)
        lab3entry.place(x=450, y=120)

        lab4 = tk.Label(self, text="مسؤول وحدة تمكين المرأة وجميع العاملين معهم", font=("thesans", 16))
        lab4.place(x=750, y=180)
        self.lab4var = tk.BooleanVar()
        lab4chk = tk.Checkbutton(self, variable=self.lab4var)
        lab4chk.place(x=700, y=180)

        lab5 = tk.Label(self, text="تطوير منظومة الكترونية لادارة احد البرامج على مستوى الجامعة او الوزارة",
                        font=("thesans", 16))
        lab5.place(x=550, y=220)
        self.lab5var = tk.BooleanVar()
        lab5chk = tk.Checkbutton(self, variable=self.lab5var)
        lab5chk.place(x=500, y=220)

        lab6 = tk.Label(self,
                        text="مدراء اقسام ضمان الجودة والاداء الجامعي وجميع العاملين معهم كمسؤولي شعب واعضاء ارتباط",
                        font=("arial", 16))
        lab6.place(x=450, y=270)
        self.lab6var = tk.BooleanVar()
        lab6chk = tk.Checkbutton(self, variable=self.lab6var)
        lab6chk.place(x=400, y=270)

        calc_button = tk.Button(self, text="حساب النقاط")
        calc_button.place(x=50, y=650)

        self.score_label = tk.Label(self, text="النقاط: 0", font=("thesans", 20))
        self.score_label.place(x=200, y=650)

        self.final_result_button = tk.Button(self, text='النتيجة النهائية', command=self.changetofinalresult)
        self.final_result_button.pack()

        def show_score():
            score = self.calculate_forth_side_score()
            self.score_label.config(text=f"النقاط: {score}", font=("thesans", 20))

        calc_button.config(command=show_score)

    def changetofinalresult(self):
        self.destroy()
        self.finalresult = FinalResult(self.master, self.login_window)
        self.finalresult.deiconify()

    def calculate_forth_side_score(self):
        score = 0

        if self.lab2var.get():
            score += 10
        if self.lab3var.get() >= 1:
            score += 10
        if self.lab4var.get():
            score += 10
        if self.lab5var.get():
            score += 10
        if self.lab6var.get():
            score += 10
        return score

class FinalResult(ctk.CTkToplevel):
    def __init__(self, master, login_window):
        super().__init__(master)
        self.login_window = login_window
        self.geometry("900x700+350+30")
        self.title('final result')
        self.username = self.login_window.username_entry.get()

        lab1 = tk.Label(self, text="النتيجة النهائية", font=("thesans", 20, "bold"))
        lab1.pack()

        display_button = tk.Button(self, text='عرض النتيجة النهائية', command=self.display_final_result)
        display_button.pack()

    def display_final_result(self):
            first_side_score = self.firstsidewindow.calculate_fisrt_side_score()
            second_side_score = self.secondsidewindow.calculate_second_side_score()
            third_side_score = self.therdsidewindow.calculate_third_side_score()
            forth_side_score = self.forthsidewindow.calculate_forth_side_score()
            total_score = first_side_score + second_side_score + third_side_score + forth_side_score
            result_label.config(text=f'نتيجة الاختبار النهائية هي {total_score}')
            result_label = tk.Label(self, text='', font=('thesans', 20))
            result_label.place(x=800, y=100)


ctk.set_appearance_mode('dark')
root = ctk.CTk()
root.config(bg='#141E46')
root.iconbitmap('icons/form.ico')
loginwindow = LoginWindow(root)
root.mainloop()
