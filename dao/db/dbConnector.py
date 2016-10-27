import pymysql
# import sys
# sys.path.insert(0, '/Users/ming.zhou/Python/workspace/Digweb/dao')
from db import Singleton

class dbConnector(Singleton.Singleton):
	def getDB(db_name):
		# print('connector is here')
		db = pymysql.connect('localhost', 'root', 'zhoum', db_name, use_unicode=True, charset='utf8')
		return db

if __name__ == '__main__':
	con1 = dbConnector()
	con2 = dbConnector()
	print(con1 == con2)
	print(con1 is con2)