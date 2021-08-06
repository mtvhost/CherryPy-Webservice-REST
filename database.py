# Created by Matheus Pabis Esteves

from getpass import getpass
from mysql.connector import connect, Error

# Alterar aqui os dados do DB
mysql_host = "localhost"
mysql_user = "admin"
mysql_password = "admin"

# Criando Banco de Dados
try:
    with connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
    ) as connection:
        create_db_query = "CREATE DATABASE paciente_imunizacao"
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)
except Error as e:
    print(e)

# Mostrando Bancos de Dados
try:
    with connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
    ) as connection:
        show_db_query = "SHOW DATABASES"
        with connection.cursor() as cursor:
            cursor.execute(show_db_query)
            for db in cursor:
                print(db)
except Error as e:
    print(e)

# Criando tabelas no BD
try:
    with connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database="paciente_imunizacao"
    ) as connection:
        create_paciente_table_query = """
        CREATE TABLE paciente (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cpf VARCHAR(11),
            nome VARCHAR(1000),
            idade INT,
            telefone VARCHAR(13)
        )
        """
        create_imunizacao_table_query = """
        CREATE TABLE imunizacao (
            id INT AUTO_INCREMENT PRIMARY KEY,
            paciente_id INT,
            lote VARCHAR(100),
            data_aplicacao VARCHAR(10),
            fabricante VARCHAR(100),
            dose_aplicada INT,
            status VARCHAR(100),
            FOREIGN KEY(paciente_id) REFERENCES paciente(id)
        )
        """
        with connection.cursor() as cursor:
            cursor.execute(create_paciente_table_query)
            cursor.execute(create_imunizacao_table_query)
            connection.commit()
except Error as e:
    print(e)

# Mostra tabela paciente
try:
    with connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database="paciente_imunizacao"
    ) as connection:
        show_table_query = "DESCRIBE paciente"
        with connection.cursor() as cursor:
            cursor.execute(show_table_query)
            # Fetch rows from last executed query
            result = cursor.fetchall()
            for row in result:
                print(row)
except Error as e:
     print(e)

# Mostra tabela imunizacao
try:
    with connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database="paciente_imunizacao"
    ) as connection:
        show_table_query = "DESCRIBE imunizacao"
        with connection.cursor() as cursor:
            cursor.execute(show_table_query)
            # Fetch rows from last executed query
            result = cursor.fetchall()
            for row in result:
                print(row)
except Error as e:
     print(e)
