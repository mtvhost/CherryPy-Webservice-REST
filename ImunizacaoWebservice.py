# Created by Matheus Pabis Esteves

import cherrypy
from getpass import getpass
from mysql.connector import connect, Error

# Alterar aqui os dados do DB
mysql_host = "localhost"
mysql_user = "admin"
mysql_password = "admin"


def validar(chaves, argumentos):
    for chave in chaves:
        if (chave not in argumentos):
            return False
    return True


class Paciente(object):

    def listar(self):
        retorno = ''
        try:
            with connect(
                host=mysql_host,
                user=mysql_user,
                password=mysql_password,
                database="paciente_imunizacao"
            ) as connection:
                select_pacientes_query = """SELECT * FROM paciente"""
                with connection.cursor() as cursor:
                    cursor.execute(select_pacientes_query)
                    # Fetch rows
                    result = cursor.fetchall()
                    for row in result:
                        retorno += ("<div>CPF: %s <br> Nome:  %s <br> Idade: %d <br> Telefone: %s <br> </div> <br>" % (
                            row[1], row[2], row[3], row[4]))
                        select_imunizacao_query = """SELECT * FROM imunizacao WHERE paciente_id = %d""" % (int(row[0]))
                        cursor.execute(select_imunizacao_query)
                        result1 = cursor.fetchall()
                        for row1 in result1:
                            retorno += ("<div> <blockquote>  Dose: %d <br> Fabricante: %s <br> Lote: %s <br> Data: %s <br> Status: %s <br> </blockquote> </div> <br>" % (
                                int(row1[5]), row1[4], row1[2], row1[3], row1[6]))

        except Error as e:
            print(e)
        return ('<html>' + retorno + '</html>')

    def inserir(self, **args):
        print(args)
        chaves = {'cpf', 'nome', 'idade', 'telefone'}
        if (validar(chaves, args)):
            try:
                with connect(
                    host=mysql_host,
                    user=mysql_user,
                    password=mysql_password,
                    database="paciente_imunizacao"
                ) as connection:
                    select_paciente_query = """SELECT id FROM paciente WHERE cpf = %s""" % (
                        args["cpf"])
                    insert_paciente_query = """INSERT INTO paciente (cpf, nome, idade, telefone) VALUES (%s, %s, %d, %s)""" % (
                        args["cpf"], args["nome"], int(args["idade"]), args["telefone"])
                    with connection.cursor() as cursor:
                        cursor.execute(select_paciente_query)
                        result = cursor.fetchall()
                        if(len(result) >= 1):
                            raise cherrypy.HTTPError(400, "Paciente já existe")
                        else:
                            cursor.execute(insert_paciente_query)
                            connection.commit()
                            cherrypy.response.status = '201'
                            return 'Criado com sucesso'
            except Error as e:
                print(e)
        else:
            raise cherrypy.HTTPError(
                400, "Parâmetros necessários estão faltando")

    def buscar(self, **args):
        print(args)
        chaves = {'cpf'}
        if (validar(chaves, args)):
            retorno = ''
            try:
                with connect(
                    host=mysql_host,
                    user=mysql_user,
                    password=mysql_password,
                    database="paciente_imunizacao"
                ) as connection:
                    select_paciente_query = """SELECT cpf, nome, idade, telefone FROM paciente WHERE cpf = %s""" % (
                        args["cpf"])
                    with connection.cursor() as cursor:
                        cursor.execute(select_paciente_query)
                        result = cursor.fetchall()
                        if(len(result) < 1):
                            raise cherrypy.HTTPError(
                                404, "Paciente não cadastrado")
                        else:
                            retorno += ("<div>CPF: %s <br> Nome:  %s <br> Idade: %d <br> Telefone: %s <br> </div>" % (
                                result[0][0], result[0][1], result[0][2], result[0][3]))
            except Error as e:
                print(e)
            return ('<html>' + retorno + '</html>')
        else:
            raise cherrypy.HTTPError(
                400, "Parâmetros necessários estão faltando")

    def atualizar(self, **args):
        print(args)
        chaves = {'cpf', 'nome', 'idade', 'telefone'}
        if (validar(chaves, args)):
            try:
                with connect(
                    host=mysql_host,
                    user=mysql_user,
                    password=mysql_password,
                    database="paciente_imunizacao"
                ) as connection:
                    select_paciente_query = """SELECT id FROM paciente WHERE cpf = %s""" % (
                        args["cpf"])
                    with connection.cursor() as cursor:
                        cursor.execute(select_paciente_query)
                        result = cursor.fetchall()
                        if(len(result) < 1):
                            raise cherrypy.HTTPError(
                                404, "Paciente não cadastrado")
                        else:
                            update_paciente_query = """UPDATE paciente SET nome = %s, idade = %d, telefone = %s WHERE id = %d""" % (
                                args["nome"], int(args["idade"]), args["telefone"], int(result[0][0]))
                            cursor.execute(update_paciente_query)
                            connection.commit()
                            cherrypy.response.status = '202'
                            return 'Atualizado com sucesso'
            except Error as e:
                print(e)
        else:
            raise cherrypy.HTTPError(
                400, "Parâmetros necessários estão faltando")


class Imunizacao(object):

    def listar(self, **args):
        print(args)
        chaves = {'cpf'}
        if (validar(chaves, args)):
            retorno = ''
            try:
                with connect(
                    host=mysql_host,
                    user=mysql_user,
                    password=mysql_password,
                    database="paciente_imunizacao"
                ) as connection:
                    select_paciente_query = """SELECT id FROM paciente WHERE cpf = %s""" % (
                        args["cpf"])
                    with connection.cursor() as cursor:
                        cursor.execute(select_paciente_query)
                        result = cursor.fetchall()
                        if(len(result) < 1):
                            raise cherrypy.HTTPError(
                                404, "Paciente não cadastrado")
                        else:
                            select_imunizacoes_query = """SELECT lote, data_aplicacao, fabricante, dose_aplicada, status FROM imunizacao WHERE paciente_id = %s""" % (
                                result[0][0])
                            cursor.execute(select_imunizacoes_query)
                            result = cursor.fetchall()
                            if(len(result) < 1):
                                raise cherrypy.HTTPError(
                                    404, "Imunizacao não cadastrado")
                            else:
                                for row in result:
                                    retorno += ("<div>Lote: %s <br> Data:  %s <br> Fabricante: %s <br> dose_aplicada: %d <br> status: %s <br> </div>" % (
                                        row[0], row[1], row[2], int(row[3]), row[4]))
            except Error as e:
                print(e)
            return ('<html>' + retorno + '</html>')
        else:
            raise cherrypy.HTTPError(
                400, "Parâmetros necessários estão faltando")

    def inserir(self, **args):
        print(args)
        chaves = {'cpf'}
        if (validar(chaves, args)):
            try:
                with connect(
                    host=mysql_host,
                    user=mysql_user,
                    password=mysql_password,
                    database="paciente_imunizacao"
                ) as connection:
                    select_paciente_query = """SELECT id FROM paciente WHERE cpf = %s""" % (
                        args["cpf"])
                    with connection.cursor() as cursor:
                        cursor.execute(select_paciente_query)
                        result = cursor.fetchall()
                        id = result[0][0]
                        if(len(result) < 1):
                            raise cherrypy.HTTPError(
                                404, "Paciente não cadastrado")
                        else:
                            select_imunizacao_query = """SELECT id FROM imunizacao WHERE paciente_id = %d""" % (
                                int(id))
                            cursor.execute(select_imunizacao_query)
                            result = cursor.fetchall()
                            if(len(result) >= 2):
                                raise cherrypy.HTTPError(400, "Imunizações já existem")
                            else:
                                insert_paciente_query = """INSERT INTO imunizacao (paciente_id, lote, data_aplicacao, fabricante, dose_aplicada, status) VALUES (%d, '', '', '', %d, 'agendamento')""" % (
                                    int(id), int(len(result)+1))
                                cursor.execute(insert_paciente_query)
                                connection.commit()
                                cherrypy.response.status = '201'
                                return 'Imunizacao criada com sucesso'
            except Error as e:
                print(e)
        else:
            raise cherrypy.HTTPError(
                400, "Parâmetros necessários estão faltando")

    def buscar(self, **args):
        print(args)
        chaves = {'cpf', 'dose_aplicada'}
        if (validar(chaves, args)):
            if(int(args['dose_aplicada']) < 1 or int(args['dose_aplicada']) > 2):
                raise cherrypy.HTTPError(404, 'Numero da dose invalida')

            retorno = ''
            try:
                with connect(
                    host=mysql_host,
                    user=mysql_user,
                    password=mysql_password,
                    database="paciente_imunizacao"
                ) as connection:
                    select_paciente_query = """SELECT id FROM paciente WHERE cpf = %s""" % (
                        args["cpf"])
                    with connection.cursor() as cursor:
                        cursor.execute(select_paciente_query)
                        result = cursor.fetchall()
                        if(len(result) < 1):
                            raise cherrypy.HTTPError(
                                404, "Paciente não cadastrado")
                        else:
                            select_imunizacoes_query = """SELECT lote, data_aplicacao, fabricante, status FROM imunizacao WHERE paciente_id = %s AND dose_aplicada = %d""" % (
                                result[0][0], int(args['dose_aplicada']))
                            cursor.execute(select_imunizacoes_query)
                            result = cursor.fetchall()
                            if(len(result) < 1):
                                raise cherrypy.HTTPError(
                                    404, "Imunizacao não cadastrado")
                            else:
                                for row in result:
                                    retorno += ("<div>Lote: %s <br> Data:  %s <br> Fabricante: %s <br> Status: %s <br> </div>" % (
                                        row[0], row[1], row[2], row[3]))
            except Error as e:
                print(e)
            return ('<html>' + retorno + '</html>')
        else:
            raise cherrypy.HTTPError(
                400, "Parâmetros necessários estão faltando")

    def atualizar(seld, **args):
        print(args)
        chaves = {'cpf', 'dose_aplicada', 'lote', 'data_aplicacao', 'fabricante'}
        if (validar(chaves, args)):

            if(int(args['dose_aplicada']) < 1 or int(args['dose_aplicada']) > 2):
                raise cherrypy.HTTPError(404, 'Numero da dose invalida')

            try:
                with connect(
                    host=mysql_host,
                    user=mysql_user,
                    password=mysql_password,
                    database="paciente_imunizacao"
                ) as connection:
                    select_imunizacao_query = """SELECT id FROM paciente WHERE cpf = %s""" % (args["cpf"])
                    with connection.cursor() as cursor:
                        cursor.execute(select_imunizacao_query)
                        result = cursor.fetchall()
                        if(len(result) < 1):
                            raise cherrypy.HTTPError(
                                404, "Paciente não cadastrado")
                        else:
                            id = int(result[0][0])
                            select_imunizacao_query =  """SELECT id FROM imunizacao WHERE paciente_id = %d AND dose_aplicada = %d""" % (id, int(args["dose_aplicada"]))
                            cursor.execute(select_imunizacao_query)
                            result = cursor.fetchall()
                            if(len(result) < 1):
                                raise cherrypy.HTTPError(404, "Imunizacao não cadastrado")
                            else:
                                update_imunizacao_query = """UPDATE imunizacao SET lote = %s, data_aplicacao = %s, fabricante = %s, status = 'aplicado' WHERE paciente_id = %d AND dose_aplicada = %d""" % (
                                    args["lote"], args["data_aplicacao"], args["fabricante"], id, int(args["dose_aplicada"]))
                                cursor.execute(update_imunizacao_query)
                                connection.commit()
                                cherrypy.response.status = '202'
                                return 'Atualizado com sucesso'
            except Error as e:
                print(e)
        else:
            raise cherrypy.HTTPError(
                400, "Parâmetros necessários estão faltando")
        


if __name__ == '__main__':

    disp = cherrypy.dispatch.RoutesDispatcher()

    P = Paciente()
    I = Imunizacao()

    disp.connect(name='listarPacientes', route='/pacientes',
                 controller=P, action='listar', conditions=dict(method=['GET']))
    disp.connect(name='inserirPaciente', route='/pacientes',
                 controller=P, action='inserir', conditions=dict(method=['POST']))
    disp.connect(name='buscarPaciente', route='/pacientes/:cpf',
                 controller=P, action='buscar', conditions=dict(method=['GET']))
    disp.connect(name='atualizarPaciente', route='/pacientes/:cpf',
                 controller=P, action='atualizar', conditions=dict(method=['PUT']))

    disp.connect(name='listarImunizacao', route='/pacientes/:cpf/imunizacao',
                 controller=I, action='listar', conditions=dict(method=['GET']))
    disp.connect(name='inserirImunizacao', route='/pacientes/:cpf/imunizacao',
                 controller=I, action='inserir', conditions=dict(method=['POST']))
    disp.connect(name='buscarImunizacao', route='/pacientes/:cpf/imunizacao/:dose_aplicada',
                 controller=I, action='buscar', conditions=dict(method=['GET']))
    disp.connect(name='atualizarImunizacao', route='/pacientes/:cpf/imunizacao/:dose_aplicada',
                 controller=I, action='atualizar', conditions=dict(method=['PUT']))

    conf = {'/': {'request.dispatch': disp}}

    cherrypy.tree.mount(root=None, config=conf)

    cherrypy.config.update({'server.socket_port': 10000})

    cherrypy.engine.start()
    cherrypy.engine.block()
