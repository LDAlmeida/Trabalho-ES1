import tkinter as tk
import pymysql.cursors
from tkinter import ttk


class SchoolRecord:

    con = 0
    c = 0

    def personal_data(self):
        self.con = pymysql.connect(host='educatorr.ccqy8084hset.sa-east-1.rds.amazonaws.com', user='admin', password='rootroot', db='educatorr',
                                   charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        self.c = self.con.cursor()

        self.c.execute("SELECT * FROM aluno WHERE Email = %s", self.Email)

        return self.c.fetchall()

    def update_tree(self):
        try:
            self.tree.delete(*self.tree.get_children())
            query = """SELECT d.Nome, ad.Nota, ad.Falta
                       FROM disciplina d, aluno_disciplina ad, aluno a
                       WHERE a.Email = %s and a.ID_aluno = ad.ID_aluno and ad.ID_disciplina = d.ID_disciplina;"""
            self.c.execute(query, self.Email)
            rows = self.c.fetchall()

            for i in range(0, len(rows)):
                if rows[i]['Nota'] == 0 and rows[i]['Falta'] == 0:
                    sit = 'Matéria Pendente'
                elif rows[i]['Nota'] < 60 and rows[i]['Falta'] > 9:
                    sit = 'Reprovado por Nota e Falta'
                elif rows[i]['Nota'] < 60:
                    sit = 'Reprovado por Nota'
                elif rows[i]['Falta'] > 9:
                    sit = 'Reprovado por Falta'
                else:
                    sit = 'Aprovado'

                if i % 2 == 0:
                    self.tree.insert("", tk.END, values=(rows[i]['Nome'], rows[i]['Nota'], rows[i]['Falta'], sit),
                                     tag='1')
                else:
                    self.tree.insert("", tk.END, values=(rows[i]['Nome'], rows[i]['Nota'], rows[i]['Falta'], sit),
                                     tag='1')
        except Exception as e4:
            print(e4, 'Não foi possível inserir na árvore!')

    def __init__(self, arg):
        self.Email = arg
        self.personalData = self.personal_data()
        self.root_school_record = tk.Tk()
        self.root_school_record.title('Histórico Escolar')
        self.root_school_record.iconbitmap("book.ico")
        self.root_school_record.geometry('600x600+350+20')
        self.root_school_record['bg'] = 'white'

        tk.Frame(self.root_school_record, bg='#66ff66', width=600, height=20).pack(side=tk.TOP)
        tk.Frame(self.root_school_record, bg='#66ff66', width=600, height=20).pack(side=tk.BOTTOM)

        tk.Label(self.root_school_record, text='UNIVERSIDADE FEDERAL DE JOÃO MONLEVADE', font='Avalon 16 bold',
                 fg='black', bg='white').pack()

        tk.Label(self.root_school_record, text='HISTÓRICO ACADÊMICO', font='Avalon 14 bold',
                 fg='black', bg='white').pack()

        tk.Label(self.root_school_record, text='Nome:', font='Ariel 10 bold',
                 fg='black', bg='white').place(x=5, y=100)
        tk.Label(self.root_school_record, text=self.personalData[0]['Nome'], font='Ariel 11',
                 fg='black', bg='white').place(x=55, y=100)

        tk.Label(self.root_school_record, text='Matrícula:', font='Ariel 10 bold',
                 fg='black', bg='white').place(x=350, y=100)
        tk.Label(self.root_school_record, text=self.personalData[0]['Num_Matricula'], font='Ariel 11',
                 fg='black', bg='white').place(x=420, y=100)

        tk.Label(self.root_school_record, text='CPF:', font='Ariel 10 bold',
                 fg='black', bg='white').place(x=5, y=140)
        tk.Label(self.root_school_record, text=self.personalData[0]['CPF'], font='Ariel 11',
                 fg='black', bg='white').place(x=45, y=140)

        tk.Label(self.root_school_record, text='RG:', font='Ariel 10 bold',
                 fg='black', bg='white').place(x=350, y=140)
        tk.Label(self.root_school_record, text=self.personalData[0]['RG'], font='Ariel 11',
                 fg='black', bg='white').place(x=380, y=140)

        tk.Label(self.root_school_record, text='Endereço:', font='Ariel 10 bold',
                 fg='black', bg='white').place(x=5, y=180)
        tk.Label(self.root_school_record, text=self.personalData[0]['Endereco'], font='Ariel 11',
                 fg='black', bg='white').place(x=75, y=180)

        tk.Label(self.root_school_record, text='Email:', font='Ariel 10 bold',
                 fg='black', bg='white').place(x=5, y=220)
        tk.Label(self.root_school_record, text=self.personalData[0]['Email'], font='Ariel 11',
                 fg='black', bg='white').place(x=50, y=220)

        self.tree = ttk.Treeview(self.root_school_record, selectmode="browse",
                                 column=("column1", "column2", "column3", "column4"), show='headings')
        self.tree.column("column1", width=200, minwidth=100, stretch=tk.NO)
        self.tree.heading("#1", text="Disciplina")
        self.tree.column("column2", width=50, minwidth=100, stretch=tk.NO)
        self.tree.heading("#2", text="Nota")
        self.tree.column("column3", width=50, minwidth=100, stretch=tk.NO)
        self.tree.heading("#3", text="Falta")
        self.tree.column("column4", width=180, minwidth=100, stretch=tk.NO)
        self.tree.heading("#4", text="Situação")
        self.tree.tag_configure('1', background='ivory2')
        self.tree.tag_configure('2', background='ivory2')
        self.tree.place(x=50, y=300)

        self.update_tree()
        self.root_school_record.mainloop()
