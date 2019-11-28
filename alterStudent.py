import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql.cursors


class ViewStudent:
    con = 0
    c = 0
    curItem = 0

    def refresh(self):
        self.update_tree()
        self.clear_entries()

    def search_record(self):
        try:
            self.tree.delete(*self.tree.get_children())

            query = " SELECT a.ID_aluno, a.Nome, a.Num_Matricula, a.CPF, a.RG, a.Endereco, c.Nome " \
                    "FROM aluno a, curso c, coordenador d WHERE a.ID_curso = c.ID_curso and d.Email = %s " \
                    "and c.ID_departamento = d.ID_departamento " \
                    "and (a.Nome like %s or a.Num_Matricula like %s or a.CPF like %s or a.RG like %s " \
                    "or a.Endereco like %s or c.Nome like %s)"
            self.c.execute(query, (self.Email, '%' + self.search_value.get() + '%', '%' + self.search_value.get() + '%',
                                               '%' + self.search_value.get() + '%', '%' + self.search_value.get() + '%',
                                               '%' + self.search_value.get() + '%',
                                               '%' + self.search_value.get() + '%'))
            rows = self.c.fetchall()

            length = str(len(rows))
            if length == 0:
                messagebox.showinfo('Alunos', 'Não foi possível encontrar um resultado!')
            else:

                for i in range(0, len(rows)):
                    if i % 2 == 0:
                        self.tree.insert("", tk.END, values=(rows[i]['ID_aluno'], rows[i]['Nome'],
                                                             rows[i]['Num_Matricula'], rows[i]['CPF'], rows[i]['RG'],
                                                             rows[i]['Endereco'], rows[i]['c.Nome']), tag='1')
                    else:
                        self.tree.insert("", tk.END, values=(rows[i]['ID_aluno'], rows[i]['Nome'],
                                                             rows[i]['Num_Matricula'], rows[i]['CPF'], rows[i]['RG'],
                                                             rows[i]['Endereco'], rows[i]['c.Nome']), tag='2')

        except Exception as e:
            print(e, "Não foi possível encontrar dados!")

    def clear_entries(self):
        self.Name_entry.delete(0, "end")
        self.Num_Matricula_entry.delete(0, "end")
        self.CPF_entry.delete(0, "end")
        self.RG_entry.delete(0, "end")
        self.Endereco_entry.delete(0, "end")
        self.ID_curso_entry.delete(0, "end")

    def delete_record(self):
        try:
            self.c.execute("SELECT ID_aluno FROM aluno WHERE Num_Matricula = %s", (self.curItem['values'][1]))
            res = self.c.fetchall()
            self.c.execute("DELETE FROM aluno_disciplina WHERE ID_aluno = %s", res[0]['ID_aluno'])
            self.c.execute("DELETE FROM aluno WHERE CPF = %s", (self.curItem['values'][2]))
            print("DADOS DELETADOS")

        except Exception as e2:
            print(e2, 'Não foi possível deletar estes dados!')

        finally:
            self.curItem = 0
            self.clear_entries()
            self.update_tree()
            self.con.commit()

    def update_record(self):
        if self.Name_value.get() != "" and self.Num_Matricula_value.get() != "" and self.CPF_value.get() != "" \
                and self.RG_value.get() != "" and self.Endereco_value.get() != "" and self.ID_curso_value.get() != "":
            try:
                self.c.execute(
                    """UPDATE aluno SET Nome = %s, Num_Matricula = %s, CPF = %s, RG = %s, Endereco = %s, 
                    ID_curso = %s WHERE Num_Matricula = %s """,
                    (self.Name_value.get(), self.Num_Matricula_value.get(), self.CPF_value.get(), self.RG_value.get(),
                     self.Endereco_value.get(), self.ID_curso_value.get(), self.curItem['values'][1]))
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

        self.Name_value.set(self.curItem['values'][0])
        self.Num_Matricula_value.set(self.curItem['values'][1])
        self.CPF_value.set(self.curItem['values'][2])
        self.RG_value.set(self.curItem['values'][3])
        self.Endereco_value.set(self.curItem['values'][4])
        self.c.execute('SELECT ID_curso FROM curso WHERE Nome = %s', self.curItem['values'][5])
        res = self.c.fetchall()
        self.ID_curso_value.set(res[0]['ID_curso'])

    def update_tree(self):
        try:
            self.tree.delete(*self.tree.get_children())
            query = "SELECT a.Nome, a.Num_Matricula, a.CPF, a.RG, a.Endereco, c.Nome " \
                    "FROM aluno a, curso c, coordenador d WHERE a.ID_curso = c.ID_curso " \
                    "and d.Email = %s and c.ID_departamento = d.ID_departamento ORDER BY a.Nome ASC"
            self.c.execute(query, self.Email)
            rows = self.c.fetchall()

            for i in range(0, len(rows)):
                if i % 2 == 0:
                    self.tree.insert("", tk.END, values=(rows[i]['Nome'], rows[i]['Num_Matricula'],
                                                         rows[i]['CPF'], rows[i]['RG'], rows[i]['Endereco'],
                                                         rows[i]['c.Nome']), tag='1')
                else:
                    self.tree.insert("", tk.END, values=(rows[i]['Nome'], rows[i]['Num_Matricula'],
                                                         rows[i]['CPF'], rows[i]['RG'], rows[i]['Endereco'],
                                                         rows[i]['c.Nome']), tag='2')
        except Exception as e4:
            print(e4, 'Não foi possível inserir na árvore!')

    def write_record(self):
        if self.Name_value.get() != "" and self.Num_Matricula_value.get() != "" and self.CPF_value.get() != "" \
                and self.RG_value.get() != "" and self.Endereco_value.get() != "" and self.ID_curso_value.get() != "":

            query = 'SELECT c.ID_curso FROM coordenador d, curso c WHERE d.Email = %s and ' \
                    'c.ID_departamento = d.ID_departamento and c.ID_curso = %s'
            self.c.execute(query, (self.Email, self.ID_curso_value.get()))
            result = self.c.fetchall()

            if result:

                try:
                    temp = self.Name_value.get().split()
                    email = temp[0].lower() + '.' + temp[-1].lower() + '@aluno.ufjm.com'

                    self.c.execute("""INSERT INTO aluno (Nome, Num_Matricula, CPF, RG, Endereco, Email, ID_curso) 
                    VALUES(%s,%s,%s,%s,%s,%s,%s) """, (self.Name_value.get(), self.Num_Matricula_value.get(),
                                                       self.CPF_value.get(), self.RG_value.get(),
                                                       self.Endereco_value.get(), email, self.ID_curso_value.get(),))
                    self.con.commit()
                    self.clear_entries()
                except pymysql.IntegrityError:
                    messagebox.showerror('Alunos', 'Este aluno já se encontra no banco de dados!')
                except Exception as e5:
                    print(e5, 'Não foi possível cadastrar aluno!')
                finally:
                    self.update_tree()
            else:
                messagebox.showerror('Alunos', 'ID do curso inválido!')
        else:
            messagebox.showwarning('Alunos', 'Favor preencher todos os campos')

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
        self.root.title('Alunos')
        self.root.resizable(False, False)
        self.root.iconbitmap("book.ico")
        self.root.geometry('+250+20')
        self.root['bg'] = '#9fff80'

        self.Name = tk.Label(self.root, text='Nome:', font='Ariel 13 bold', fg='white', bg='#9fff80')
        self.Name.grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Name_value = tk.StringVar(self.root, value="")
        self.Name_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.Name_value)
        self.Name_entry.grid(row=0, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.Num_Matricula = tk.Label(self.root, text='Nº Matrícula:', font='Ariel 13 bold', fg='white',
                                      bg='#9fff80')
        self.Num_Matricula.grid(row=1, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Num_Matricula_value = tk.StringVar(self.root, value="")
        self.Num_Matricula_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.Num_Matricula_value)
        self.Num_Matricula_entry.grid(row=1, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.CPF = tk.Label(self.root, text='CPF:', font='Ariel 13 bold', fg='white', bg='#9fff80')
        self.CPF.grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.CPF_value = tk.StringVar(self.root, value="")
        self.CPF_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.CPF_value)
        self.CPF_entry.grid(row=2, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.RG = tk.Label(self.root, text='RG:', font='Ariel 13 bold', fg='white', bg='#9fff80')
        self.RG.grid(row=3, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.RG_value = tk.StringVar(self.root, value="")
        self.RG_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.RG_value)
        self.RG_entry.grid(row=3, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.Endereco = tk.Label(self.root, text='Endereço:', font='Ariel 13 bold', fg='white', bg='#9fff80')
        self.Endereco.grid(row=4, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Endereco_value = tk.StringVar(self.root, value="")
        self.Endereco_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.Endereco_value)
        self.Endereco_entry.grid(row=4, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.ID_curso = tk.Label(self.root, text='ID do Curso:', font='Ariel 13 bold', fg='white', bg='#9fff80')
        self.ID_curso.grid(row=5, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.ID_curso_value = tk.StringVar(self.root, value="")
        self.ID_curso_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.ID_curso_value)
        self.ID_curso_entry.grid(row=5, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.submit_button = ttk.Button(self.root, text='Cadastrar', cursor="hand2", command=self.write_record)
        self.submit_button.grid(row=0, column=3, padx=9, sticky=tk.W + tk.E)

        self.update_button = ttk.Button(self.root, text='Atualizar', cursor="hand2", command=self.update_record)
        self.update_button.grid(row=1, column=3, padx=9, sticky=tk.W + tk.E)

        self.delete_button = ttk.Button(self.root, text='Deletar', cursor="hand2", command=self.delete_record)
        self.delete_button.grid(row=2, column=3, padx=9, sticky=tk.W + tk.E)

        self.tree = ttk.Treeview(self.root, selectmode="browse",
                                 column=("column1", "column2", "column3", "column4", "column5", "column6"),
                                 show='headings')
        self.tree.column("column1", width=180, minwidth=100, stretch=tk.NO)
        self.tree.heading("#1", text="Nome")
        self.tree.column("column2", width=100, minwidth=100, stretch=tk.NO)
        self.tree.heading("#2", text="Num_Matricula")
        self.tree.column("column3", width=120, minwidth=100, stretch=tk.NO)
        self.tree.heading("#3", text="CPF")
        self.tree.column("column4", width=100, minwidth=100, stretch=tk.NO)
        self.tree.heading("#4", text="RG")
        self.tree.column("column5", width=250, minwidth=100, stretch=tk.NO)
        self.tree.heading("#5", text="Endereco")
        self.tree.column("column6", width=120, minwidth=100, stretch=tk.NO)
        self.tree.heading("#6", text="Curso")
        self.tree.bind("<ButtonRelease-1>", self.select_item)
        self.tree.bind("<space>", self.select_item)
        self.tree.tag_configure('1', background='ivory2')
        self.tree.tag_configure('2', background='ivory2')
        self.tree.grid(row=6, column=0, padx=9, pady=9, sticky=tk.W + tk.E, columnspan=4)

        tk.Label(self.root, text='Pesquisar:', font='Ariel 13 bold', fg='white', bg='#9fff80').grid(row=7, column=0,
                                                                                                    columnspan=2,
                                                                                                    sticky=tk.E,
                                                                                                    padx=9, pady=9)
        self.search_value = tk.StringVar(self.root, value="")
        tk.Entry(self.root, textvariable=self.search_value).grid(row=7, column=2, sticky=tk.W + tk.E, padx=9, pady=9)

        self.search_button = ttk.Button(self.root, text='Pesquisar', cursor="hand2", command=self.search_record)
        self.search_button.grid(row=7, column=3, padx=9, sticky=tk.W + tk.E)

        self.refresh_button = ttk.Button(self.root, text='Atualizar', cursor="hand2", command=self.refresh)
        self.refresh_button.grid(row=8, column=2, padx=9, pady=9, sticky=tk.W + tk.E)

        self.back_button = ttk.Button(self.root, text='Voltar', cursor="hand2", command=self.back)
        self.back_button.grid(row=8, column=3, padx=9, sticky=tk.W + tk.E)

        self.setup_db()
        self.root.mainloop()
