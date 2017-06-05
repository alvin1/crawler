import MySQLdb
import uuid
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

    def query(self, command, params=()):
        try:
            self.cursor.execute(command, params)
            rows = self.cursor.fetchall()
            columns = self.cursor.description

            data_set = []
            schema = []
            for row in rows:
                row_data = {}
                index = 0
                for col in columns:
                    schema.append({
                        'field_name': col[0],
                        'data_type': col[1]
                    })
                    row_data[col[0]] = row[index]
                    index += 1
                data_set.append(row_data)

            return {
                'schema': schema,
                'data': data_set
            }
        except Exception, e:
            print(e.message)
            return None

    def close(self):
        self.conn.close()

    def generate_id(self):
        return uuid.uuid1()