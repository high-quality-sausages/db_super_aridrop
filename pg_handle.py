import traceback

import psycopg2


class PgHandler(object):
    def __init__(self, db="postgres", user="postgres",
                 password=None, host="127.0.0.1", port="5432"):
        '''
        Args:
            db: Database
            user: Username
            password: Password
            host: Server
            port: Port
        '''
        self.db = db
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.config = f'dbname = {self.db} \
                        user = {self.user} \
                        password = {self.password} \
                        host = {self.host} \
                        port = {self.port}'

    def query(self, sql):
        '''query sql'''
        try:
            conn = psycopg2.connect(self.config)
            cur = conn.cursor()
            cur.execute(sql)
            res = cur.fetchall()
            cur.close()
            conn.close()
            if not res:
                res = []
            return res
        except psycopg2.Error as e:
            print(str(traceback.format_exc()))
            return

    def execute(self, sql):
        '''execute sql'''

        try:
            conn = psycopg2.connect(self.config)
            cur = conn.cursor()
            cur.execute(sql)
            res = None
            if "returning" in sql:
                res = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
            return res
        except psycopg2.Error as e:
            print(str(traceback.format_exc()))

    def create_database(self, db_name):
        '''
        build a new database
        Args:
            db_name: name of the database you want to create
        Raises:
            psycopg2.errors.DuplicateDatabase: database "{db_name}" already exists
        '''
        conn = psycopg2.connect(self.config)
        conn.autocommit = True

        cur = conn.cursor()
        cur.execute(f'CREATE DATABASE {db_name};')
        cur.close()

    def drop_database(self, db_name):
        '''
        build a new database
        Args:
            db_name: name of the database you want to drop
        Raises:
            psycopg2.errors.InvalidCatalogName: database "{db_name}" does not exist
        '''
        conn = psycopg2.connect(self.config)
        conn.autocommit = True

        cur = conn.cursor()
        cur.execute(f'DROP DATABASE {db_name};')
        cur.close()


if __name__ == "__main__":
    pg = PgHandler("postgres", "postgres", "0000")
    pg.drop_database('hah')
