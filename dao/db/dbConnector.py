import pymysql
import sys
sys.path.insert(0, '/Users/ming.zhou/Python/workspace/Digweb/dao')
from db import Singleton

class dbConnector(Singleton.Singleton):
	def getDB(db_name):
		# print('connector is here')
		#localhost = 127.0.0.1，root表示的是数据库用户名，zhoum表示的是数据库密码，db_name表示的是数据库名，
		# use_unicode使用unicode编码，charset=’utf-8‘
		db = pymysql.connect('localhost', 'root', 'zhoum', db_name, use_unicode=True, charset='utf8')
		return db

if __name__ == '__main__':
	con1 = dbConnector()
	con2 = dbConnector()
	print(con1)
	print(con2)
	print(con1 == con2)
	print(con1 is con2)