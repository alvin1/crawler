import MySQLdb
from settings import Settings


class DatabaseHelper():
    def __init__(self):
        self.conn = MySQLdb.connect(host=Settings.DB_HOST, port=Settings.DB_PORT, user=Settings.DB_USER,
                                    passwd=Settings.DB_PASSWD, db=Settings.DB_NAME, charset="utf8")
        self.cursor = self.conn.cursor()

    def execute(self, command, params=()):
        try:
            self.cursor.execute(command, params)
            self.conn.commit()
        except Exception, e:
            self.conn.rollback()
            raise

    def close(self):
        self.conn.close()