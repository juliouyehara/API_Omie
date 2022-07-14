import psycopg2 as pg
import psycopg2.extras


def insert_postgre_elastic(key_postgre, response):
    try:
        connection = pg.connect(key_postgre)
        curs = connection.cursor()
        postgres_insert_query = """INSERT INTO accountify_omie  (cnpj_cpf_nu, 
                                                        categoria,
                                                        codigo_vendedor,
                                                        grupo,
                                                        parcela,
                                                        status,
                                                        data_emissao,
                                                        data_pagamento,
                                                        data_previsao,
                                                        codigo_cliente,
                                                        valor,
                                                        nome_fantasia,
                                                        nome_categoria,
                                                        nome_vendedor) 
        VALUES (%(cnpj)s, 
                %(categoria)s,
                %(codigo vendedor)s,
                %(grupo)s,
                %(parcela)s,
                %(status)s,
                %(data emissao)s,
                %(data pagamento)s,
                %(data previsao)s,
                %(codigo cliente)s,
                %(valor)s,
                %(nome fantasia)s,
                %(nome categoria)s,
                %(vendedores)s)"""
        pg.extras.execute_batch(curs, postgres_insert_query, response, page_size=len(response))
        connection.commit()
        count = curs.rowcount
        print(count, "Record inserted successfully into mobile table")
        curs.close()
        connection.close()
        print("PostgreSQL connection is closed")
        print(f'Dados inseridos na tabela, a partir de')

    except (Exception, pg.Error) as error:
        print("Failed to insert record into mobile table", error)