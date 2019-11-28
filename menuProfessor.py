import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pymysql.cursors
from update_class import UpdateClass


class MenuProfessor:

    con = 0
    c = 0

    def discovery_departament(self):
        self.con = pymysql.connect(host='educatorr.ccqy8084hset.sa-east-1.rds.amazonaws.com', user='admin', password='rootroot', db='educatorr',
                                   charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        self.c = self.con.cursor()

        query = "SELECT d.Nome FROM professor p, departamento d WHERE p.Email = %s " \
                "and d.ID_departamento = p.ID_departamento"

        self.c.execute(query, self.Email)
        res = self.c.fetchall()

        return res[0]['Nome']

    def quit_window(self):
        if messagebox.askokcancel('Educatorr', 'Deseja realmente sair?'):
            self.root_professor.destroy()

    def update_class(self):
        UpdateClass(self.Email)

    def __init__(self, arg):
        self.Email = arg
        self.root_professor = tk.Tk()
        self.root_professor.title('Menu do Professor')
        self.root_professor.protocol("WM_DELETE_WINDOW", self.quit_window)
        self.root_professor.iconbitmap("book.ico")
        self.root_professor.geometry('600x600+350+20')
        self.root_professor['bg'] = 'white'

        self.top_frame = tk.Frame(self.root_professor, bg='#66ff66', width=600, height=100).pack(side=tk.TOP)
        tk.Frame(self.root_professor, bg='#66ff66', width=600, height=20).pack(side=tk.BOTTOM)

        tk.Label(self.top_frame, text='Educatorr', font='Avalon 25 bold', bg='#66ff66', fg='white').place(x=0, y=0)

        self.datetime = datetime.now()
        self.dt = self.datetime.strftime('%d/%m/%Y %H:%M')

        tk.Label(self.top_frame, text=self.dt, font='Avalon 10 bold', bg='#66ff66', fg='white').place(x=480, y=0)

        tk.Label(self.top_frame, text=self.Email, font='Avalon 10 bold', bg='#66ff66', fg='white').place(x=0, y=40)

        self.Nome_Departamento = 'Professor(a) do ' + self.discovery_departament()

        tk.Label(self.top_frame, text=self.Nome_Departamento, font='Avalon 10 bold',
                 bg='#66ff66', fg='white').place(x=0, y=60)

        tk.Button(self.root_professor, width=20, text='Disciplinas', bg='#66ff66', fg='white', font='Avalon 13', bd=2,
                  relief='ridge', activeforeground='#66ff66', activebackground='white',
                  cursor="hand2", command=self.update_class).place(x=210, y=200)
        tk.Button(self.root_professor, width=20, text='Sair', bg='#66ff66', fg='white', font='Avalon 13', bd=2,
                  relief='ridge', activeforeground='#66ff66', activebackground='white',
                  cursor="hand2", command=self.quit_window).place(x=210, y=250)

        self.root_professor.mainloop()
