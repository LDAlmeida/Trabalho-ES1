import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pymysql.cursors
from menuStudent import MenuStudent
from menuProfessor import MenuProfessor
from menuCoordinator import MenuCoordinator
from student_class import StudentClass


class LoginWindow:
    con = 0
    c = 0

    def clear_entries(self):
        self.Name_Sign_entry.delete(0, "end")
        self.Email_Sign_entry.delete(0, "end")
        self.Password_Sign_entry.delete(0, "end")

    def login(self):

        self.con = pymysql.connect(host='educatorr.ccqy8084hset.sa-east-1.rds.amazonaws.com', user='admin', password='rootroot', db='educatorr',
                                   charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        self.c = self.con.cursor()

        query = 'SELECT Email FROM login WHERE Name = %s and Password = %s;'

        self.c.execute(query, (self.Name_Login_value.get(), self.Password_Login_value.get()))

        result = self.c.fetchall()

        if not result:
            messagebox.showerror('Educatorr', 'Nome de usuário ou senha incorreta!')
        else:
            if '@aluno' in result[0]['Email']:
                self.root.destroy()
                MenuStudent(result[0]['Email'])
                LoginWindow()
            elif '@prof' in result[0]['Email']:
                self.root.destroy()
                MenuProfessor(result[0]['Email'])
                LoginWindow()
            else:
                self.root.destroy()
                MenuCoordinator(result[0]['Email'])
                LoginWindow()

    def signin_up(self):

        self.con = pymysql.connect(host='educatorr.ccqy8084hset.sa-east-1.rds.amazonaws.com', user='admin', password='rootroot', db='educatorr',
                                   charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        self.c = self.con.cursor()

        aux = False

        if '@coord' in self.Email_Sign_value.get():
            query = 'SELECT Email FROM coordenador WHERE EMAIL = %s'
            self.c.execute(query, self.Email_Sign_value.get())
            result = self.c.fetchall()
            if result:
                aux = True

        elif '@aluno' in self.Email_Sign_value.get():
            query = 'SELECT Email FROM aluno WHERE EMAIL = %s'
            self.c.execute(query, self.Email_Sign_value.get())
            result = self.c.fetchall()
            if result:
                aux = True

        elif '@prof' in self.Email_Sign_value.get():
            query = 'SELECT Email FROM professor WHERE EMAIL = %s'
            self.c.execute(query, self.Email_Sign_value.get())
            result = self.c.fetchall()
            if result:
                aux = True

        if aux:
            query = 'INSERT INTO login (Name, Email, Password) VALUES (%s, %s, %s)'

            try:
                self.c.execute(query, (self.Name_Sign_value.get(), self.Email_Sign_value.get(),
                                       self.Password_Sign_value.get()))
                self.con.commit()
                self.clear_entries()
                messagebox.showinfo('Educatorr', 'Usuário cadastrado!')

            except pymysql.IntegrityError:
                messagebox.showerror('Educatorr', 'Este usuário já se encontra no banco de dados!')
            except Exception as e:
                print(e, 'Não foi possível inserir usuário no banco de dados!')
        else:
            messagebox.showwarning('Educatorr', 'Apenas integrantes da universidade podem ser cadastrados!')

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Login')
        self.root.iconbitmap("book.ico")
        self.root.geometry('600x600+350+20')
        self.root['bg'] = '#66ff66'

        tk.Label(self.root, text='Educatorr', font='Helvetica 28 bold', bg='#66ff66', fg='white').place(x=210, y=100)

        self.canvas = tk.Canvas(self.root, height=350, width=2, bg='#4dff4d')
        self.line = self.canvas.create_line(300, 0, 300, 20)
        self.canvas.place(x=300, y=200)

        tk.Label(self.root, text='Nome de Usuário', font='Ariel 12 bold', bg='#66ff66', fg='white').place(x=75, y=220)
        self.Name_Login_value = tk.StringVar()
        self.Name_Login_entry = ttk.Entry(self.root, width=30, textvariable=self.Name_Login_value)
        self.Name_Login_entry.place(x=50, y=250)

        tk.Label(self.root, text='Senha', font='Ariel 12 bold', bg='#66ff66', fg='white').place(x=110, y=290)
        self.Password_Login_value = tk.StringVar()
        self.Password_Login_entry = ttk.Entry(self.root, width=30, show='*', textvariable=self.Password_Login_value)
        self.Password_Login_entry.place(x=50, y=320)

        tk.Button(self.root, text='Entrar', bg='#66ff66', fg='white', width=15, bd=2, font='Avalon 11 bold',
                  activeforeground='#66ff66', activebackground='white', relief=tk.RIDGE,
                  cursor="hand2", command=self.login).place(x=70, y=380)

        tk.Label(self.root, text='Nome de Usuário', font='Ariel 12 bold', bg='#66ff66', fg='white').place(x=375, y=220)
        self.Name_Sign_value = tk.StringVar()
        self.Name_Sign_entry = ttk.Entry(self.root, width=30, textvariable=self.Name_Sign_value)
        self.Name_Sign_entry.place(x=350, y=250)

        tk.Label(self.root, text='Email', font='Ariel 12 bold', bg='#66ff66', fg='white').place(x=415, y=290)
        self.Email_Sign_value = tk.StringVar()
        self.Email_Sign_entry = ttk.Entry(self.root, width=30, textvariable=self.Email_Sign_value)
        self.Email_Sign_entry.place(x=350, y=320)

        tk.Label(self.root, text='Senha', font='Ariel 12 bold', bg='#66ff66', fg='white').place(x=410, y=360)
        self.Password_Sign_value = tk.StringVar()
        self.Password_Sign_entry = ttk.Entry(self.root, width=30, textvariable=self.Password_Sign_value)
        self.Password_Sign_entry.place(x=350, y=390)

        tk.Button(self.root, text='Cadastrar-se', bg='#66ff66', fg='white', width=15, bd=2, font='Avalon 11 bold',
                  activeforeground='#66ff66', activebackground='white', relief=tk.RIDGE,
                  command=self.signin_up, cursor="hand2").place(x=370, y=450)

        StudentClass()
        self.root.mainloop()


try:
    LoginWindow()
except Exception as ex:
    print(ex, 'Não foi possível abrir a janela!')
