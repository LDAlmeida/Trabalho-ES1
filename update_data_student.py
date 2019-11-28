import tkinter as tk
import pymysql.cursors
from tkinter import ttk
from tkinter import messagebox


class UpdateData:

    con = 0
    c = 0

    def search_db(self):
        self.con = pymysql.connect(host='educatorr.ccqy8084hset.sa-east-1.rds.amazonaws.com', user='admin', password='rootroot', db='educatorr',
                                   charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        self.c = self.con.cursor()

        self.c.execute("SELECT Nome, CPF, RG, Endereco FROM aluno WHERE Email = %s", self.Email)
        return self.c.fetchall()

    def update(self):

        try:
            query = "UPDATE aluno SET Nome = %s, CPF = %s, RG = %s, Endereco = %s WHERE Email = %s"
            self.c.execute(query, (self.name_var.get(), self.cpf_var.get(), self.rg_var.get(), self.address_var.get(),
                                   self.Email))
            messagebox.showinfo('Atualização', f'Os dados foram atualizados, {self.name_var.get()}')
            self.up_data.destroy()
        except pymysql.IntegrityError:
            messagebox.showerror('Aluno', 'Este aluno já se encontra no banco de dados!')
        except Exception as e:
            print(e, 'Não foi possível atualizar os dados!')
        finally:
            self.con.commit()

    def __init__(self, arg):
        self.Email = arg
        self.up_data = tk.Toplevel()
        self.up_data.title('Atualizar Dados')
        self.up_data.iconbitmap("book.ico")
        self.up_data.geometry('380x350+450+50')
        self.up_data['bg'] = 'white'

        tk.Label(self.up_data, text='Atualizar seus dados', font='Ariel 15 bold', fg='#66ff66',
                 bg='white').grid(row=0, column=0, columnspan=2, sticky=tk.W + tk.E, pady=20, padx=80)

        tk.Label(self.up_data, text='Nome', font='Ariel 12 bold', fg='#66ff66',
                 bg='white').grid(row=1, column=0, padx=5, pady=5)

        tk.Label(self.up_data, text='CPF', font='Ariel 12 bold', fg='#66ff66',
                 bg='white').grid(row=2, column=0, padx=5, pady=5)

        tk.Label(self.up_data, text='RG', font='Ariel 12 bold', fg='#66ff66',
                 bg='white').grid(row=3, column=0, padx=5, pady=5)

        tk.Label(self.up_data, text='Endereço', font='Ariel 12 bold', fg='#66ff66',
                 bg='white').grid(row=4, column=0, padx=5, pady=5)

        self.name_var = tk.StringVar(self.up_data, value="")
        self.name_entry = ttk.Entry(self.up_data, width=30, textvariable=self.name_var)
        self.name_entry.grid(row=1, column=1)

        self.cpf_var = tk.StringVar(self.up_data, value="")
        self.cpf_entry = ttk.Entry(self.up_data, width=30, textvariable=self.cpf_var)
        self.cpf_entry.grid(row=2, column=1)

        self.rg_var = tk.StringVar(self.up_data, value="")
        self.rg_entry = ttk.Entry(self.up_data, width=30, textvariable=self.rg_var)
        self.rg_entry.grid(row=3, column=1)

        self.address_var = tk.StringVar(self.up_data, value="")
        self.address_entry = ttk.Entry(self.up_data, width=30, textvariable=self.address_var)
        self.address_entry.grid(row=4, column=1)

        res = self.search_db()

        self.name_var.set(res[0]['Nome'])
        self.cpf_var.set(res[0]['CPF'])
        self.rg_var.set(res[0]['RG'])
        self.address_var.set(res[0]['Endereco'])

        tk.Button(self.up_data, width=10, text='Editar', bg='#66ff66', fg='white', font='Avalon 13', bd=2,
                  relief='ridge', activeforeground='#66ff66', activebackground='white',
                  cursor="hand2", command=self.update).grid(row=5, column=0, columnspan=2, pady=30)

        self.up_data.mainloop()
