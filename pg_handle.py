import traceback

import psycopg2


class PgHandler(object):
    '''
    make sure your postgre server is available
    Attributes:
        db: Database
        user: Username
        password: Password
        host: Server
        port: Port
    '''

    def __init__(self, db="postgres", user="postgres",
                 password=None, host="127.0.0.1", port=5432):
        self.db = db
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.config = f'dbname = {self.db} \
                        user = {self.user} \
                        password = {self.password} \
                        host = {self.host} \
                        port = {self.port} '

    def __connect(self):
        return psycopg2.connect(self.config)

    def query(self, sql):
        '''query sql'''
        try:
            conn = self.__connect()
            cur = conn.cursor()
            cur.execute(sql)
            result = cur.fetchall()
            cur.close()
            conn.close()
            if not result:
                result = []
            return result
        except psycopg2.Error as e:
            print(str(traceback.format_exc()))
            return

    def execute(self, sql):
        '''execute sql'''

        try:
            conn = self.__connect()
            cur = conn.cursor()
            cur.execute(sql)
            result = None
            if "returning" in sql:
                result = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
            return result
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
        conn = self.__connect()
        conn.autocommit = True

        cur = conn.cursor()
        result = cur.execute(f'CREATE DATABASE {db_name};')
        cur.close()
        return result

    def drop_database(self, db_name):
        '''
        build a new database
        Args:
            db_name: name of the database you want to drop
        Raises:
            psycopg2.errors.InvalidCatalogName: database "{db_name}" does not exist
            Exception: drop database "{db_name}" failed
        '''

        assert db_name != 'postgres', \
            '''drop database 'postgres' is not available'''

        conn = self.__connect()
        conn.autocommit = True

        cur = conn.cursor()
        print(f'You are dropping database {db_name}! (y/N)')
        confirm = input()
        if confirm == 'y' or 'Y':
            try:
                cur.execute(f'DROP DATABASE {db_name};')
                cur.close()
            except:
                raise Exception(f'drop database "{db_name}" failed')
        else:
            return

    def rebuild_database(self, db_name):
        '''
        drop and create a new database '{db_name}'
        Args:
            db_name: name of the database you want to rebuild
        Raises:
            psycopg2.errors.InvalidCatalogName: database "{db_name}" does not exist
            Exception: rebuild database "{db_name}" failed
        '''

        assert db_name != 'postgres', \
            '''rebuild database 'postgres' is not available'''
        conn = self.__connect()
        conn.autocommit = True
        cur = conn.cursor()
        print(f'You are rebuilding database {db_name}! (y/N)')
        confirm = input()
        if confirm == 'y' or 'Y':
            try:
                cur.execute(f'DROP DATABASE {db_name};')
                cur.execute(f'CREATE DATABASE {db_name};')
            except:
                raise Exception(f'rebuild database "{db_name}" failed')
        else:
            return


if __name__ == "__main__":
    pg = PgHandler("moviesite", "postgres", "0000")
    # print(pg.query("select * from comments_comment"))
    pg.drop_database('test_db')
    # pg.rebuild_database('hah')
