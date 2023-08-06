import os
from configparser import ConfigParser

from kindenty.base.DatabaseType import DatabaseType
from kindenty.base.DatabasePool import Pool

type = DatabaseType.mysql
# pool = Pool(database="/sqlit3Data.db", isolation_level=None)
# pool = Pool(check_same_thread=False)
# pool = Pool(db_type=DatabaseType.mysql, host='localhost', user='admin', password='123456', database='cats_strategy',
#             cursorclass=pymysql.cursors.DictCursor)
print('root Path: %s' % os.getcwd())
configParser = ConfigParser()
configParser.read('conf/config.ini')
host = configParser.get('database', 'host')
user = configParser.get('database', 'userName')
password = configParser.get('database', 'password')
database = configParser.get('database', 'database')
driverName = configParser.get('database', 'driverName')

pool = Pool(maxActive=15, db_type=DatabaseType[driverName], host=host, user=user, password=password,
            database=database, autocommit=True)
