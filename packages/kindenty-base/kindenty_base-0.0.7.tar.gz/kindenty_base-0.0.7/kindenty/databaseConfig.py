from kindenty.base.DatabaseType import DatabaseType
from kindenty.base.DatabasePool import Pool

type = DatabaseType.mysql
# pool = Pool(database="/sqlit3Data.db", isolation_level=None)
# pool = Pool(check_same_thread=False)
# pool = Pool(db_type=DatabaseType.mysql, host='localhost', user='admin', password='123456', database='cats_strategy',
#             cursorclass=pymysql.cursors.DictCursor)
pool = Pool(maxActive=15, db_type=DatabaseType.mysql, host='192.168.1.133', user='root', password='123456', database='cats_strategy', autocommit=True)