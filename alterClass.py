import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql.cursors


class ViewClass:
    con = 0
    c = 0
    curItem = 0

    def refresh(self):
        self.update_tree()
        self.clear_entries()

    def search_record(self):
        try:
            self.tree.delete(*self.tree.get_children())

            query = "SELECT disc.ID_disciplina, disc.Nome, disc.Professor, cur.Nome " \
                    "FROM disciplina disc, coordenador c, curso cur " \
                    "WHERE disc.ID_curso = cur.ID_curso " \
                    "and c.Email = %s and cur.ID_departamento = c.ID_departamento " \
                    "and (disc.Nome like %s or disc.Professor like %s or cur.Nome like %s)"
            self.c.execute(query, (self.Email, '%' + self.search_value.get() + '%', '%' + self.search_value.get() + '%',
                                               '%' + self.search_value.get() + '%',))
            rows = self.c.fetchall()

            length = str(len(rows))
            if length == 0:
                messagebox.showinfo('Disciplinas', 'Não foi possível encontrar um resultado!')
            else:

                for i in range(0, len(rows)):
                    if i % 2 == 0:
                        self.tree.insert("", tk.END, values=(rows[i]['ID_disciplina'], rows[i]['Nome'],
                                                             rows[i]['Professor'], rows[i]['cur.Nome']), tag='1')
                    else:
                        self.tree.insert("", tk.END, values=(rows[i]['ID_disciplina'], rows[i]['Nome'],
                                                             rows[i]['Professor'], rows[i]['cur.Nome']), tag='2')

        except Exception as e:
            print(e, "Não foi possível encontrar dados!")

    def clear_entries(self):
        self.Name_entry.delete(0, "end")
        self.Professor_entry.delete(0, "end")
        self.Curso_entry.delete(0, "end")

    def delete_record(self):
        try:
            self.c.execute("DELETE FROM disciplina WHERE ID_disciplina = %s", (self.curItem['values'][0]))
            print("DADOS DELETADOS")

        except Exception as e2:
            print(e2, 'Não foi possível deletar estes dados!')

        finally:
            self.curItem = 0
            self.clear_entries()
            self.update_tree()
            self.con.commit()

    def update_record(self):
        if self.Name_value.get() != "" and self.Curso_value.get() != "":
            try:
                res = None
                if self.Professor_value.get() != '':
                    self.c.execute("SELECT * FROM professor WHERE Nome = %s", self.Professor_value.get())
                    res = self.c.fetchall()

                if res:
                    query = "UPDATE disciplina SET Nome = %s, Professor = %s, ID_curso = %s " \
                            "WHERE Nome = %s;"
                    self.c.execute(query, (self.Name_value.get(), self.Professor_value.get(), self.Curso_value.get(),
                                           self.curItem['values'][0]))
                    self.clear_entries()
                    print('Dados atualizados!')
                else:
                    messagebox.showwarning('Professor', 'Este professor não está cadastrado no banco de dados!')

            except pymysql.IntegrityError:
                messagebox.showerror('Disciplinas', 'Esta disciplina já se encontra no banco de dados!')
            except Exception as e3:
                print(e3, 'Não foi possível atualizar os dados!')
            finally:
                self.update_tree()
                self.con.commit()
        else:
            messagebox.showwarning('Disciplinas', 'Favor preencher os campos Nome e Id do curso')

    def select_item(self, *args):
        self.curItem = self.tree.item(self.tree.focus())
        print(self.curItem)

        self.Name_value.set(self.curItem['values'][0])
        self.Professor_value.set(self.curItem['values'][1])
        self.c.execute('SELECT ID_curso FROM curso WHERE Nome = %s', self.curItem['values'][2])
        res = self.c.fetchall()
        self.Curso_value.set(res[0]['ID_curso'])

    def update_tree(self):
        try:
            self.tree.delete(*self.tree.get_children())
            query = "SELECT p.Nome, p.Professor, d.Nome " \
                    "FROM disciplina p, curso d, coordenador c WHERE p.ID_curso = d.ID_curso " \
                    "and c.Email = %s and d.ID_departamento = c.ID_departamento ORDER BY d.Nome ASC, p.Nome ASC"
            self.c.execute(query, self.Email)
            rows = self.c.fetchall()

            for i in range(0, len(rows)):
                if i % 2 == 0:
                    self.tree.insert("", tk.END, values=(rows[i]['Nome'],
                                                         rows[i]['Professor'], rows[i]['d.Nome']), tag='1')
                else:
                    self.tree.insert("", tk.END, values=(rows[i]['Nome'],
                                                         rows[i]['Professor'], rows[i]['d.Nome']), tag='2')
        except Exception as e4:
            print(e4, 'Não foi possível inserir na árvore!')

    def write_record(self):
        if self.Name_value.get() != "" and self.Curso_value.get() != "":

            query = "SELECT r.ID_curso FROM curso r, coordenador c WHERE c.Email = %s and " \
                    "c.ID_departamento = r.ID_departamento and r.ID_curso = %s"

            self.c.execute(query, (self.Email, self.Curso_value.get()))
            result = self.c.fetchall()

            if result:

                try:
                    res = None
                    if self.Professor_value.get() != '':
                        self.c.execute("SELECT * FROM professor WHERE Nome = %s", self.Professor_value.get())
                        res = self.c.fetchall()

                    if res:
                        self.c.execute("""INSERT INTO disciplina (Nome, Professor, ID_curso)  VALUES(%s,%s,%s) """,
                                       (self.Name_value.get(), self.Professor_value.get(), self.Curso_value.get()))
                        self.con.commit()
                        self.clear_entries()
                    else:
                        messagebox.showwarning('Professor', 'Este professor não está cadastrado no banco de dados!')

                except pymysql.IntegrityError:
                    messagebox.showerror('Disciplinas', 'Esta disciplina já se encontra no banco de dados!')
                except Exception as e5:
                    print(e5, 'Não foi possível cadastrar disciplina!')
                finally:
                    self.update_tree()
            else:
                messagebox.showerror('Disciplinas', 'Id do curso inválido!')
        else:
            messagebox.showwarning('Disciplinas', 'Os campos nome e Id do curso são obrigatórios o preenchimento!')

    def setup_db(self):
        try:
            self.con = pymysql.connect(host='educatorr.ccqy8084hset.sa-east-1.rds.amazonaws.com', user='admin', password='rootroot', db='educatorr',
                                   charset='utf8', cursorclass=pymysql.cursors.DictCursor)
            self.c = self.con.cursor()

            self.con.commit()
            self.update_tree()

        except Exception as e6:
            print(e6, 'Não foi possível conectar ao banco de dados!')

    def back(self):
        self.root.destroy()

    def __init__(self, arg):

        self.Email = arg
        self.root = tk.Tk()
        self.root.title('Disciplinas')
        self.root.resizable(False, False)
        self.root.iconbitmap("book.ico")
        self.root.geometry('+350+20')
        self.root['bg'] = '#9fff80'

        self.Name = tk.Label(self.root, text='Nome:', font='Ariel 13 bold', fg='white', bg='#9fff80')
        self.Name.grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Name_value = tk.StringVar(self.root, value="")
        self.Name_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.Name_value)
        self.Name_entry.grid(row=0, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.Professor = tk.Label(self.root, text='Professor:', font='Ariel 13 bold', fg='white', bg='#9fff80')
        self.Professor.grid(row=1, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Professor_value = tk.StringVar(self.root, value=" ")
        self.Professor_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.Professor_value)
        self.Professor_entry.grid(row=1, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.Curso = tk.Label(self.root, text='ID do Curso:', font='Ariel 13 bold', fg='white', bg='#9fff80')
        self.Curso.grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Curso_value = tk.StringVar(self.root, value="")
        self.Curso_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.Curso_value)
        self.Curso_entry.grid(row=2, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.submit_button = ttk.Button(self.root, text='Cadastrar', cursor="hand2", command=self.write_record)
        self.submit_button.grid(row=0, column=3, padx=9, sticky=tk.W + tk.E)

        self.update_button = ttk.Button(self.root, text='Atualizar', cursor="hand2", command=self.update_record)
        self.update_button.grid(row=1, column=3, padx=9, sticky=tk.W + tk.E)

        self.delete_button = ttk.Button(self.root, text='Deletar', cursor="hand2", command=self.delete_record)
        self.delete_button.grid(row=2, column=3, padx=9, sticky=tk.W + tk.E)

        self.tree = ttk.Treeview(self.root, selectmode="browse",
                                 column=("column1", "column2", "column3"), show='headings')
        self.tree.column("column1", width=200, minwidth=100, stretch=tk.NO)
        self.tree.heading("#1", text="Nome")
        self.tree.column("column2", width=200, minwidth=100, stretch=tk.NO)
        self.tree.heading("#2", text="Professor")
        self.tree.column("column3", width=200, minwidth=100, stretch=tk.NO)
        self.tree.heading("#3", text="Curso")
        self.tree.bind("<ButtonRelease-1>", self.select_item)
        self.tree.bind("<space>", self.select_item)
        self.tree.tag_configure('1', background='ivory2')
        self.tree.tag_configure('2', background='ivory2')
        self.tree.grid(row=4, column=0, padx=9, pady=9, sticky=tk.W + tk.E, columnspan=4)

        tk.Label(self.root, text='Pesquisar:', font='Ariel 13 bold', fg='white', bg='#9fff80').grid(row=5, column=0,
                                                                                                    columnspan=2,
                                                                                                    sticky=tk.E,
                                                                                                    padx=9, pady=9)
        self.search_value = tk.StringVar(self.root, value="")
        tk.Entry(self.root, textvariable=self.search_value).grid(row=5, column=2, sticky=tk.W + tk.E, padx=9, pady=9)

        self.search_button = ttk.Button(self.root, text='Pesquisar', cursor="hand2", command=self.search_record)
        self.search_button.grid(row=5, column=3, padx=9, sticky=tk.W + tk.E)

        self.refresh_button = ttk.Button(self.root, text='Atualizar', cursor="hand2", command=self.refresh)
        self.refresh_button.grid(row=6, column=2, padx=9, pady=9, sticky=tk.W + tk.E)

        self.back_button = ttk.Button(self.root, text='Voltar', cursor="hand2", command=self.back)
        self.back_button.grid(row=6, column=3, padx=9, sticky=tk.W + tk.E)

        self.setup_db()
        self.root.mainloop()
