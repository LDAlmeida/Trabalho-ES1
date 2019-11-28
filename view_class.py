import tkinter as tk
import pymysql.cursors
from tkinter import ttk


class ViewClass:

    con = 0
    c = 0

    def name(self):
        self.con = pymysql.connect(host='educatorr.ccqy8084hset.sa-east-1.rds.amazonaws.com', user='admin', password='rootroot', db='educatorr',
                                   charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        self.c = self.con.cursor()

        res = None

        try:
            self.c.execute("SELECT Nome, Num_Matricula FROM aluno WHERE Email = %s", self.Email)
            res = self.c.fetchall()
        except Exception as e:
            print(e, 'Não foi possível encontrar Aluno!')
        finally:
            return res

    def update_tree(self):
        try:
            self.tree.delete(*self.tree.get_children())
            query = """SELECT d.Professor, c.Nome, d.Nome AS nome_d, ad.Nota, ad.Falta
                       FROM disciplina d, curso c, aluno_disciplina ad, aluno a
                       WHERE a.Email = %s and a.ID_aluno = ad.ID_aluno and ad.ID_disciplina = d.ID_disciplina 
                       and d.ID_curso = c.ID_curso;"""
            self.c.execute(query, self.Email)
            rows = self.c.fetchall()

            for i in range(0, len(rows)):
                if i % 2 == 0:
                    self.tree.insert("", tk.END, values=(rows[i]['Professor'], rows[i]['Nome'],
                                                         rows[i]['nome_d'], rows[i]['Nota'], rows[i]['Falta']),
                                     tag='1')
                else:
                    self.tree.insert("", tk.END, values=(rows[i]['Professor'], rows[i]['Nome'],
                                                         rows[i]['nome_d'], rows[i]['Nota'], rows[i]['Falta']),
                                     tag='2')
        except Exception as e4:
            print(e4, 'Não foi possível inserir na árvore!')

    def __init__(self, arg):
        self.Email = arg
        self.name_student = self.name()
        self.view_class = tk.Tk()
        self.view_class.title('Disciplinas')
        self.view_class.iconbitmap("book.ico")
        self.view_class.geometry('+350+20')
        self.view_class.resizable(False, False)
        self.view_class['bg'] = '#66ff66'

        self.name_class = tk.Label(self.view_class, text='Disciplinas', font='Avalon 16 bold', fg='white',
                                   bg='#66ff66')
        self.name_class.grid(row=0, column=0, columnspan=4, sticky=tk.W+tk.E, padx=80, pady=50)

        tk.Label(self.view_class, text='Nome: ' + self.name_student[0]['Nome'], bg='#66ff66', fg='white',
                 font='Ariel 12 bold').grid(row=1, column=0)
        tk.Label(self.view_class, text='Matrícula: ' + self.name_student[0]['Num_Matricula'], bg='#66ff66', fg='white',
                 font='Ariel 12 bold').grid(row=1, column=1)

        self.tree = ttk.Treeview(self.view_class, selectmode="browse",
                                 column=("column1", "column2", "column3", "column4", "column5"),
                                 show='headings')
        self.tree.column("column1", width=200, minwidth=100, stretch=tk.NO)
        self.tree.heading("#1", text="Professor")
        self.tree.column("column2", width=150, minwidth=100, stretch=tk.NO)
        self.tree.heading("#2", text="Curso")
        self.tree.column("column3", width=180, minwidth=100, stretch=tk.NO)
        self.tree.heading("#3", text="Disciplina")
        self.tree.column("column4", width=50, minwidth=100, stretch=tk.NO)
        self.tree.heading("#4", text="Nota")
        self.tree.column("column5", width=50, minwidth=100, stretch=tk.NO)
        self.tree.heading("#5", text="Falta")
        self.tree.tag_configure('1', background='ivory2')
        self.tree.tag_configure('2', background='ivory2')
        self.tree.grid(row=2, column=0, padx=10, pady=10, columnspan=4)

        self.update_tree()
        self.view_class.mainloop()
