import pymysql.cursors


class StudentClass:

    c = 0
    con = 0

    def populate_database(self):
        self.con = pymysql.connect(host='educatorr.ccqy8084hset.sa-east-1.rds.amazonaws.com', user='admin', password='rootroot', db='educatorr',
                                   charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        self.c = self.con.cursor()

        try:
            self.c.execute("""SELECT ID_aluno, ID_curso FROM aluno""")
            res1 = self.c.fetchall()

            self.c.execute("""SELECT ID_disciplina, ID_curso FROM disciplina""")
            res2 = self.c.fetchall()

            for i in res1:
                for j in res2:
                    self.c.execute("SELECT * FROM aluno_disciplina WHERE ID_aluno = %s and ID_disciplina = %s",
                                   (i['ID_aluno'], j['ID_disciplina']))
                    result = self.c.fetchall()

                    if not result:
                        if i['ID_curso'] == j['ID_curso']:
                            self.c.execute("INSERT INTO aluno_disciplina (ID_aluno, ID_disciplina, Nota, Falta) "
                                           "VALUES (%s, %s, %s, %s)", (i['ID_aluno'], j['ID_disciplina'], 0, 0))

        except Exception as e:
            print(e, 'Não foi possível povoar o banco!')

        finally:
            self.con.commit()

    def __init__(self):
        self.populate_database()


StudentClass()
