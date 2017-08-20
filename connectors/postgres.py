import psycopg2
from connector import Connector

class Postgres(Connector):
    '''Connector for Postgres databases'''

    def __init__(self, connectionJson):
        self.database = connectionJson['database']
        self.user = connectionJson['user']
        self.password = connectionJson['password']
        self.host = connectionJson['host'] if 'host' in connectionJson else 'localhost'
        self.port = connectionJson['port'] if 'port' in connectionJson else '5432'

    def connect(self):
        self.connection = psycopg2.connect(database=self.database, user=self.user, password=self.password,
                                      host=self.host, port=self.port)
        self.cursor = self.connection.cursor()

    def configureStore(self, sample):
        fields = ''

        for aggregate in sample:
            fieldType = type(aggregate['value']).__name__
            value = aggregate['value']

            if isinstance(value, float):
                fieldType = 'real'
            elif isinstance(value, dict) or isinstance(value, list):
                fieldType = 'jsonb'
            elif isinstance(value, str):
                fieldType = 'text'

            fields += ',{} {}'.format(aggregate['field'], fieldType)

        print fields

    def createRecord(self):
        pass
