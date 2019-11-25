import update
import tabelas

tupla = []
table = int(input("Tabela que será alterada: "))

if table == 1:
    print("\n### MODO DE ALTERAÇÃO ###\n\n")
    opcao = int(input("1 INSERIR\n2 DELETAR\n3 EDITAR\n\n"))
    if opcao == 1:
        tupla = tabelas.departamento()
        update.inserir(tupla, table)
    elif opcao == 2:
        tupla = tabelas.departamento()
        update.deletar(tupla, table)
    elif opcao == 3:
        tupla = tabelas.departamento()
        update.editar(tupla, table)
    else:
        print("Opção inválida!")

elif table == 2:
    print("\n### MODO DE ALTERAÇÃO ###\n")
    opcao = int(input("1 INSERIR\n2 DELETAR\n3 EDITAR\n\n"))
    if opcao == 1:
        tupla = tabelas.professor()
        update.inserir(tupla, table)
    elif opcao == 2:
        tupla = tabelas.professor()
        update.deletar(tupla, table)
    elif opcao == 3:
        tupla = tabelas.professor()
        update.editar(tupla, table)
    else:
        print("Opção inválida!")

elif table == 3:
    print("\n### MODO DE ALTERAÇÃO ###\n\n")
    opcao = int(input("1 INSERIR\n2 DELETAR\n3 EDITAR\n\n"))
    if opcao == 1:
        tupla = tabelas.aluno()
        update.inserir(tupla, table)
    elif opcao == 2:
        tupla = tabelas.aluno()
        update.deletar(tupla, table)
    elif opcao == 3:
        tupla = tabelas.aluno()
        update.editar(tupla, table)
    else:
        print("Opção inválida!")

elif table == 4:
    print("\n### MODO DE ALTERAÇÃO ###\n\n")
    opcao = int(input("1 INSERIR\n2 DELETAR\n3 EDITAR\n\n"))
    if opcao == 1:
        tupla = tabelas.disciplina()
        update.inserir(tupla, table)
    elif opcao == 2:
        tupla = tabelas.disciplina()
        update.deletar(tupla, table)
    elif opcao == 3:
        tupla = tabelas.disciplina()
        update.editar(tupla, table)
    else:
        print("Opção inválida!")

elif table == 5:
    print("\n### MODO DE ALTERAÇÃO ###\n\n")
    opcao = int(input("1 INSERIR\n2 DELETAR\n3 EDITAR\n\n"))
    if opcao == 1:
        tupla = tabelas.curso()
        update.inserir(tupla, table)
    elif opcao == 2:
        tupla = tabelas.curso()
        update.deletar(tupla, table)
    elif opcao == 3:
        tupla = tabelas.curso()
        update.editar(tupla, table)
    else:
        print("Opção inválida!")

else:
    print("OPÇÃO INVÁLIDA!")