import os
import logging
import psycopg2
import psycopg2.extras
from psycopg2 import sql


logger = logging.getLogger("__name__")


conn = psycopg2.connect(
    host=os.environ['DB_HOST'],
    port=os.environ['DB_PORT'],
    user=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD'],
    database="crossplane_examples",
    )


def version():
    print('Connecting to the PostgreSQL database...')
    cur = conn.cursor()
    print('PostgreSQL database version:')
    cur.execute('SELECT version()')
    db_version = cur.fetchone()
    print(db_version)
    cur.close()
    return db_version


def create_tables():
    command = "CREATE TABLE USERS(ID SERIAL, FIRST_NAME TEXT NOT NULL, LAST_NAME TEXT NOT NULL)"
    cur = conn.cursor()
    try:
        cur.execute(command)
    except Exception as e:
        print(e)
        logger.error(e)
    cur.close()
    conn.commit()


def insert_user(first_name, last_name):
    sql = "INSERT INTO users(first_name, last_name) VALUES(%s, %s) RETURNING id;"
    cur = conn.cursor()
    cur.execute(sql, (first_name, last_name))
    id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return id


def insert_users(users):
    sql = "INSERT INTO users(first_name, last_name) VALUES(%s, %s)"
    cur = conn.cursor()
    cur.executemany(sql, users)
    conn.commit()
    cur.close()


def select_users():
    # (use sql.SQL() to prevent SQL injection attack)
    statement = sql.SQL(
        "SELECT * FROM {};"
    ).format(
        sql.Identifier('users')
    )
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(statement)
    users = cur.fetchall()
    cur.close()
    return users


if __name__ == '__main__':
    try:
        version()
#        create_tables(conn)
        insert_user("Eric", 'Charles')
        insert_users(
            [
                ('John', 'Doe'),
                ('Foo', 'Bar'),
            ]
        )
        users = select_users()
        for num, row in enumerate(users):
            print (f"row: {num} {row}")
            print (row['first_name'])

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
