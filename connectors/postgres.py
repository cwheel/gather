import psycopg2
from connector import Connector

class Postgres(Connector):
    '''Connector for Postgres databases'''

    def __init__(self, connectionJson, patternName):
        self.database = connectionJson['database']
        self.user = connectionJson['user']
        self.password = connectionJson['password']
        self.host = connectionJson['host'] if 'host' in connectionJson else 'localhost'
        self.port = connectionJson['port'] if 'port' in connectionJson else '5432'
        self.table = patternName

        self.connect()

    def connect(self):
        self.connection = psycopg2.connect(database=self.database, user=self.user, password=self.password,
                                      host=self.host, port=self.port)
        self.cursor = self.connection.cursor()

    def configureStore(self, aggregateResults):
        try:
            self.cursor.execute('SELECT * FROM {}'.format(self.table))
        except psycopg2.ProgrammingError:
            fields = ''

            for sample in aggregateResults:
                fieldType = type(sample['value']).__name__
                value = sample['value']

                if isinstance(value, float):
                    fieldType = 'real'
                elif isinstance(value, dict) or isinstance(value, list):
                    fieldType = 'jsonb'
                elif isinstance(value, str):
                    fieldType = 'text'

                fields += ',"{}" {}'.format(sample['field'], fieldType)

            query = 'CREATE TABLE {} ("id" serial,  PRIMARY KEY ("id") {})'.format(self.table, fields)

            self.connection.rollback()
            self.cursor.execute(query)
            self.connection.commit()

    def createRecord(self, aggregateResults):
        fields = ','.join(['"{}"'.format(sample['field']) for sample in aggregateResults])
        values = ','.join([self.__safeValue(sample['value']) for sample in aggregateResults])

        query = 'INSERT INTO {} ({}) VALUES ({})'.format(self.table, fields, values)

        self.cursor.execute(query)
        self.connection.commit()

    def __safeValue(self, value):
        strVal = str(value)

        if isinstance(value, int) or isinstance(value, float) or isinstance(value, bool):
            return strVal
        else:
            return '"{}"'.format(strVal)
