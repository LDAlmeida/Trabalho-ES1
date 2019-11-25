import update

def departamento():
    dados = []
    
    nome = input("Nome do departamento: ")
    codigo = int(input("Código do departamento: "))
    gcpf = int(input("CPF do gerente: "))
    dados = [codigo, nome, gcpf]
    
    return dados

def professor():
    dados = []
    
    nome = input("Nome do professor: ")
    cpf = int(input("CPF do professor: "))
    dnr = int(input("Número do departamento: "))
    dados = [cpf, nome, dnr]

    return dados

def aluno():
    dados = []
    
    nome = input("Nome do aluno: ")
    matricula = int(input("Matrícula do aluno: "))
    cod_curso = int(input("Código do curso: "))
    dados = [matricula, nome, cod_curso]

    return dados

def disciplina():
    dados = []
    
    nome = input("Nome da disciplina: ")
    codigo = int(input("Código da disciplina: "))
    dnr = int(input("Departamento da disciplina: "))
    dados = [codigo, nome, dnr]

    return dados

def curso():
    dados = []
    
    nome = input("Nome do curso: ")
    codigo = int(input("Código do curso: "))
    dnr = int(input("Departamento do curso: "))
    dados = [codigo, nome, dnr]

    return dados
