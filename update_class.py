import tkinter as tk
import pymysql.cursors
from tkinter import ttk
from tkinter import messagebox


class UpdateClass:

    con = 0
    c = 0
    curItem = 0

    def clear_entries(self):
        self.points_entry.delete(0, "end")
        self.absences_entry.delete(0, "end")

    def update_record(self):
        if self.points_value.get() != "" and self.absences_value.get() != "":
            try:
                self.c.execute("UPDATE aluno_disciplina SET Nota = %s, Falta = %s WHERE ID_aluno = %s and "
                               "ID_disciplina = %s", (self.points_value.get(), self.absences_value.get(),
                                                      self.name_student.get(), self.name_class.get()))
                self.clear_entries()
                print('Dados atualizados!')
            except pymysql.IntegrityError:
                messagebox.showerror('Alunos', 'Este aluno já se encontra no banco de dados!')
            except Exception as e3:
                print(e3, 'Não foi possível atualizar os dados!')
            finally:
                self.update_tree()
                self.con.commit()
        else:
            messagebox.showwarning('Alunos', 'Favor preencher todos os campos')

    def select_item(self, *args):
        self.curItem = self.tree.item(self.tree.focus())
        print(self.curItem)

        self.c.execute("SELECT a.ID_aluno, d.ID_disciplina FROM aluno a, disciplina d "
                       "WHERE a.Nome = %s and d.Nome = %s", (self.curItem['values'][0], self.curItem['values'][2]))
        res = self.c.fetchall()
        self.name_student.set(res[0]['ID_aluno'])
        self.name_class.set(res[0]['ID_disciplina'])
        self.points_value.set(self.curItem['values'][3])
        self.absences_value.set(self.curItem['values'][4])

    def create_list(self):
        self.con = pymysql.connect(host='educatorr.ccqy8084hset.sa-east-1.rds.amazonaws.com', user='admin', password='rootroot', db='educatorr',
                                   charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        self.c = self.con.cursor()

        res = []
        try:
            query = """SELECT d.Nome
                       FROM disciplina d, professor p
                       WHERE p.Email = %s and p.Nome = d.Professor;"""
            self.c.execute(query, self.Email)
            result = self.c.fetchall()

            for i in result:
                res.append(i['Nome'])
            return res

        except Exception as e:
            messagebox.showinfo(e, 'Este professor não leciona nenhuma aula atualmente!')
            return res

    def update_tree(self):

        try:
            self.tree.delete(*self.tree.get_children())
            query = """SELECT a.Nome AS aluno, c.Nome, d.Nome AS nome_d, ad.Nota, ad.Falta
                       FROM disciplina d, curso c, aluno_disciplina ad, aluno a, professor p
                       WHERE p.Email = %s and p.Nome = d.Professor and d.ID_disciplina = ad.ID_disciplina 
                       and ad.ID_aluno = a.ID_aluno and d.Nome = %s and d.ID_curso = c.ID_curso;"""
            self.c.execute(query, (self.Email, self.classVar.get()))
            rows = self.c.fetchall()

            for i in range(0, len(rows)):
                if i % 2 == 0:
                    self.tree.insert("", tk.END, values=(rows[i]['aluno'], rows[i]['Nome'],
                                                         rows[i]['nome_d'], rows[i]['Nota'], rows[i]['Falta']),
                                     tag='1')
                else:
                    self.tree.insert("", tk.END, values=(rows[i]['aluno'], rows[i]['Nome'],
                                                         rows[i]['nome_d'], rows[i]['Nota'], rows[i]['Falta']),
                                     tag='2')
        except Exception as e4:
            print(e4, 'Não foi possível inserir na árvore!')

    def __init__(self, arg):
        self.Email = arg
        self.list_class = self.create_list()
        self.update_class = tk.Tk()
        self.update_class.title('Disciplinas')
        self.update_class.iconbitmap("book.ico")
        self.update_class.geometry('+350+20')
        self.update_class.resizable(False, False)
        self.update_class['bg'] = '#66ff66'

        self.name_class = tk.Label(self.update_class, text='Disciplinas', font='Avalon 18 bold', fg='white',
                                   bg='#66ff66')
        self.name_class.grid(row=0, column=0, columnspan=4, sticky=tk.W + tk.E, padx=80, pady=20)

        self.classVar = tk.StringVar(self.update_class)
        self.classVar.set(self.list_class[0])
        self.option_class = tk.OptionMenu(self.update_class, self.classVar, *self.list_class)
        self.option_class.grid(row=1, column=0, padx=40, pady=20)
        self.option_class.configure(width=30, bg='#66ff66', fg='white', activebackground='white',
                                    activeforeground='black', cursor="hand2")

        tk.Button(self.update_class, width=15, text='Escolher', bg='#66ff66', fg='white', font='Avalon 13', bd=2,
                  relief='ridge', activeforeground='#66ff66', activebackground='white',
                  cursor="hand2", command=self.update_tree).grid(row=1, column=1, sticky=tk.W + tk.E, columnspan=2,
                                                                 padx=10, pady=20)

        self.name_student = tk.StringVar(self.update_class, value="")
        self.name_class = tk.StringVar(self.update_class, value="")

        self.points = tk.Label(self.update_class, text='Nota:', font='Ariel 13 bold', fg='white', bg='#66ff66')
        self.points.grid(row=3, column=0, padx=10, pady=10)

        self.points_value = tk.StringVar(self.update_class, value="")
        self.points_entry = ttk.Entry(self.update_class, font='Ariel, 10', textvariable=self.points_value)
        self.points_entry.grid(row=3, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.absences = tk.Label(self.update_class, text='Faltas:', font='Ariel 13 bold', fg='white', bg='#66ff66')
        self.absences.grid(row=4, column=0, padx=10, pady=10)

        self.absences_value = tk.StringVar(self.update_class, value="")
        self.absences_entry = ttk.Entry(self.update_class, font='Ariel, 10', textvariable=self.absences_value)
        self.absences_entry.grid(row=4, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        tk.Button(self.update_class, width=15, text='Atualizar', bg='#66ff66', fg='white', font='Avalon 13', bd=2,
                  relief='ridge', activeforeground='#66ff66', activebackground='white',
                  cursor="hand2", command=self.update_record).grid(row=5, column=1, sticky=tk.W + tk.E, columnspan=2,
                                                                   padx=10, pady=10)

        self.tree = ttk.Treeview(self.update_class, selectmode="browse",
                                 column=("column1", "column2", "column3", "column4", "column5"),
                                 show='headings')
        self.tree.column("column1", width=200, minwidth=100, stretch=tk.NO)
        self.tree.heading("#1", text="Aluno")
        self.tree.column("column2", width=150, minwidth=100, stretch=tk.NO)
        self.tree.heading("#2", text="Curso")
        self.tree.column("column3", width=180, minwidth=100, stretch=tk.NO)
        self.tree.heading("#3", text="Disciplina")
        self.tree.column("column4", width=50, minwidth=100, stretch=tk.NO)
        self.tree.heading("#4", text="Nota")
        self.tree.column("column5", width=50, minwidth=100, stretch=tk.NO)
        self.tree.heading("#5", text="Falta")
        self.tree.bind("<ButtonRelease-1>", self.select_item)
        self.tree.bind("<space>", self.select_item)
        self.tree.tag_configure('1', background='ivory2')
        self.tree.tag_configure('2', background='ivory2')
        self.tree.grid(row=6, column=0, padx=10, pady=10, columnspan=4)

        self.update_tree()
        self.update_class.mainloop()
