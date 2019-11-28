import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pymysql.cursors
from update_data_student import UpdateData
from view_class import ViewClass
from school_record import SchoolRecord


class MenuStudent:

    con = 0
    c = 0

    def discovery_class(self):
        self.con = pymysql.connect(host='educatorr.ccqy8084hset.sa-east-1.rds.amazonaws.com', user='admin', password='rootroot', db='educatorr',
                                   charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        self.c = self.con.cursor()

        try:

            query = "SELECT c.Nome FROM aluno a, curso c WHERE a.Email = %s " \
                    "and a.ID_curso = c.ID_curso"

            self.c.execute(query, self.Email)
            res = self.c.fetchall()

            return res[0]['Nome']
        except Exception as ex:
            print(ex, 'Aluno não cadastrado!')

    def quit_window(self):
        if messagebox.askokcancel('Educatorr', 'Deseja realmente sair?'):
            self.root_student.destroy()

    def update_data(self):
        UpdateData(self.Email)

    def view_class(self):
        ViewClass(self.Email)

    def school_record(self):
        SchoolRecord(self.Email)

    def __init__(self, arg):
        self.Email = arg
        self.root_student = tk.Tk()
        self.root_student.title('Menu do Aluno')
        self.root_student.protocol("WM_DELETE_WINDOW", self.quit_window)
        self.root_student.iconbitmap("book.ico")
        self.root_student.geometry('600x600+350+20')
        self.root_student['bg'] = 'white'

        self.top_frame = tk.Frame(self.root_student, bg='#66ff66', width=600, height=100).pack(side=tk.TOP)
        tk.Frame(self.root_student, bg='#66ff66', width=600, height=20).pack(side=tk.BOTTOM)

        tk.Label(self.top_frame, text='Educatorr', font='Avalon 25 bold', bg='#66ff66', fg='white').place(x=0, y=0)

        self.datetime = datetime.now()
        self.dt = self.datetime.strftime('%d/%m/%Y %H:%M')

        tk.Label(self.top_frame, text=self.dt, font='Avalon 10 bold', bg='#66ff66', fg='white').place(x=480, y=0)

        tk.Label(self.top_frame, text=self.Email, font='Avalon 10 bold', bg='#66ff66', fg='white').place(x=0, y=40)

        self.Nome_Curso = 'Aluno(a) do Curso de ' + self.discovery_class()

        tk.Label(self.top_frame, text=self.Nome_Curso, font='Avalon 10 bold',
                 bg='#66ff66', fg='white').place(x=0, y=60)

        tk.Button(self.root_student, width=20, text='Atualizar Dados', bg='#66ff66', fg='white', font='Avalon 13', bd=2,
                  relief='ridge', activeforeground='#66ff66', activebackground='white',
                  cursor="hand2", command=self.update_data).place(x=210, y=200)
        tk.Button(self.root_student, width=20, text='Disciplinas', bg='#66ff66', fg='white', font='Avalon 13', bd=2,
                  relief='ridge', activeforeground='#66ff66', activebackground='white',
                  cursor="hand2", command=self.view_class).place(x=210, y=250)
        tk.Button(self.root_student, width=20, text='Gerar Histórico', bg='#66ff66', fg='white', font='Avalon 13',
                  bd=2, relief='ridge', activeforeground='#66ff66', activebackground='white',
                  cursor="hand2", command=self.school_record).place(x=210, y=300)
        tk.Button(self.root_student, width=20, text='Sair', bg='#66ff66', fg='white', font='Avalon 13', bd=2,
                  relief='ridge', activeforeground='#66ff66', activebackground='white',
                  cursor="hand2", command=self.quit_window).place(x=210, y=350)

        self.root_student.mainloop()
