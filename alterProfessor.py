import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql.cursors


class ViewProfessor:
    con = 0
    c = 0
    curItem = 0

    def refresh(self):
        self.update_tree()
        self.clear_entries()

    def search_record(self):
        try:
            self.tree.delete(*self.tree.get_children())

            query = " SELECT p.ID_professor, p.Nome, p.CPF, p.Especialidade, d.Nome" \
                    "FROM professor p, coordenador c, departamento d WHERE d.ID_departamento = p.ID_departamento" \
                    "c.Email = %s and c.ID_departamento = p.ID_departamento " \
                    "and (p.Nome like %s or p.CPF like %s or p.Especialidade like %s or d.Nome like %s)"
            self.c.execute(query, (self.Email, '%' + self.search_value.get() + '%', '%' + self.search_value.get() + '%',
                                               '%' + self.search_value.get() + '%',
                                               '%' + self.search_value.get() + '%'))
            rows = self.c.fetchall()

            length = str(len(rows))
            if length == 0:
                messagebox.showinfo('Professores', 'Não foi possível encontrar um resultado!')
            else:

                for i in range(0, len(rows)):
                    if i % 2 == 0:
                        self.tree.insert("", tk.END, values=(rows[i]['ID_professor'], rows[i]['Nome'],
                                                             rows[i]['CPF'], rows[i]['Especialidade'],
                                                             rows[i]['d.Nome']), tag='1')
                    else:
                        self.tree.insert("", tk.END, values=(rows[i]['ID_professor'], rows[i]['Nome'],
                                                             rows[i]['CPF'], rows[i]['Especialidade'],
                                                             rows[i]['d.Nome']), tag='2')

        except Exception as e:
            print(e, "Não foi possível encontrar dados!")

    def clear_entries(self):
        self.Name_entry.delete(0, "end")
        self.CPF_entry.delete(0, "end")
        self.Especialidade_entry.delete(0, "end")

    def delete_record(self):
        try:
            self.c.execute("UPDATE disciplina SET Professor = %s WHERE Professor = %s", ("", self.curItem['values'][0]))
            self.c.execute("DELETE FROM professor WHERE CPF = %s", (self.curItem['values'][1]))
            print("DADOS DELETADOS")

        except Exception as e2:
            print(e2, 'Não foi possível deletar estes dados!')

        finally:
            self.curItem = 0
            self.clear_entries()
            self.update_tree()
            self.con.commit()

    def update_record(self):
        if self.Name_value.get() != "" and self.CPF_value.get() != "" and self.Especialidade_value.get() != "":
            try:
                query = "UPDATE professor SET Nome = %s, CPF = %s, Especialidade = %s WHERE CPF = %s;"
                self.c.execute(query, (self.Name_value.get(), self.CPF_value.get(), self.Especialidade_value.get(),
                                       self.curItem['values'][1]))
                self.clear_entries()
                print('Dados atualizados!')
            except pymysql.IntegrityError:
                messagebox.showerror('Professores', 'Este professor já se encontra no banco de dados!')
            except Exception as e3:
                print(e3, 'Não foi possível atualizar os dados!')
            finally:
                self.update_tree()
                self.con.commit()
        else:
            messagebox.showwarning('Professores', 'Favor preencher todos os campos')

    def select_item(self, *args):
        self.curItem = self.tree.item(self.tree.focus())
        print(self.curItem)

        self.Name_value.set(self.curItem['values'][0])
        self.CPF_value.set(self.curItem['values'][1])
        self.Especialidade_value.set(self.curItem['values'][2])

    def update_tree(self):
        try:
            self.tree.delete(*self.tree.get_children())
            query = "SELECT p.Nome, p.CPF, p.Especialidade, d.Nome " \
                    "FROM professor p, departamento d, coordenador c WHERE p.ID_departamento = d.ID_departamento " \
                    "and c.Email = %s and d.ID_departamento = c.ID_departamento ORDER BY p.Nome ASC"
            self.c.execute(query, self.Email)
            rows = self.c.fetchall()

            for i in range(0, len(rows)):
                if i % 2 == 0:
                    self.tree.insert("", tk.END, values=(rows[i]['Nome'], rows[i]['CPF'],
                                                         rows[i]['Especialidade'], rows[i]['d.Nome']), tag='1')
                else:
                    self.tree.insert("", tk.END, values=(rows[i]['Nome'], rows[i]['CPF'],
                                                         rows[i]['Especialidade'], rows[i]['d.Nome']), tag='2')
        except Exception as e4:
            print(e4, 'Não foi possível inserir na árvore!')

    def write_record(self):
        if self.Name_value.get() != "" and self.CPF_value.get() != "" and self.Especialidade_value.get() != "":

            try:
                self.c.execute("SELECT ID_departamento FROM coordenador WHERE Email = %s", self.Email)
                res = self.c.fetchall()

                temp = self.Name_value.get().split()
                email = temp[0].lower() + '.' + temp[-1].lower() + '@prof.ufjm.com'
                self.c.execute("""INSERT INTO professor (Nome, CPF, Especialidade, Email, ID_departamento) 
                VALUES(%s,%s,%s,%s,%s) """, (self.Name_value.get(), self.CPF_value.get(),
                                             self.Especialidade_value.get(), email,
                                             res[0]['ID_departamento'],))
                self.con.commit()
                self.clear_entries()
            except pymysql.IntegrityError:
                messagebox.showerror('Professores', 'Este professor já se encontra no banco de dados!')
            except Exception as e5:
                print(e5, 'Não foi possível cadastrar professor!')
            finally:
                self.update_tree()
        else:
            messagebox.showwarning('Professores', 'Favor preencher todos os campos')

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
        self.root.title('Professores')
        self.root.resizable(False, False)
        self.root.iconbitmap("book.ico")
        self.root.geometry('+350+20')
        self.root['bg'] = '#9fff80'

        self.Name = tk.Label(self.root, text='Nome:', font='Ariel 13 bold', fg='white', bg='#9fff80')
        self.Name.grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Name_value = tk.StringVar(self.root, value="")
        self.Name_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.Name_value)
        self.Name_entry.grid(row=0, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.CPF = tk.Label(self.root, text='CPF:', font='Ariel 13 bold', fg='white', bg='#9fff80')
        self.CPF.grid(row=1, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.CPF_value = tk.StringVar(self.root, value="")
        self.CPF_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.CPF_value)
        self.CPF_entry.grid(row=1, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.Especialidade = tk.Label(self.root, text='Ramo:', font='Ariel 13 bold', fg='white', bg='#9fff80')
        self.Especialidade.grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Especialidade_value = tk.StringVar(self.root, value="")
        self.Especialidade_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.Especialidade_value)
        self.Especialidade_entry.grid(row=2, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.submit_button = ttk.Button(self.root, text='Cadastrar', cursor="hand2", command=self.write_record)
        self.submit_button.grid(row=0, column=3, padx=9, sticky=tk.W + tk.E)

        self.update_button = ttk.Button(self.root, text='Atualizar', cursor="hand2", command=self.update_record)
        self.update_button.grid(row=1, column=3, padx=9, sticky=tk.W + tk.E)

        self.delete_button = ttk.Button(self.root, text='Deletar', cursor="hand2", command=self.delete_record)
        self.delete_button.grid(row=2, column=3, padx=9, sticky=tk.W + tk.E)

        self.tree = ttk.Treeview(self.root, selectmode="browse",
                                 column=("column1", "column2", "column3", "column4"), show='headings')
        self.tree.column("column1", width=180, minwidth=100, stretch=tk.NO)
        self.tree.heading("#1", text="Nome")
        self.tree.column("column2", width=120, minwidth=100, stretch=tk.NO)
        self.tree.heading("#2", text="CPF")
        self.tree.column("column3", width=180, minwidth=100, stretch=tk.NO)
        self.tree.heading("#3", text="Especialidade")
        self.tree.column("column4", width=200, minwidth=100, stretch=tk.NO)
        self.tree.heading("#4", text="Departamento")
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
