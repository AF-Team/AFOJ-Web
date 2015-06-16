# coding=utf-8
import MySQLdb

class GetTaskMySQL(object):
	"""将需要判定的内容从数据库中取出，将数据传给TaskSender"""
	def __init__(self):
		self.conn = MySQLdb.connect(user='oj', passwd='oj', db='afoj', use_unicode=True)
		self.cursor = self.conn.cursor()
		self.cursor.execute("set names utf8")
		self.conn.commit()
	def Update(self,information):
		RunID=information[0]
		time=information[1]
		memory=information[2]
		result=information[3]
		sql = "update status_solution set time=%d, memory=%d, result=%d where id=%d"  %(time,memory,result,RunID)   
		print sql
		self.cursor.execute(sql) 
		self.conn.commit() 
	def UpdateToCompile(self,RunID):
		sql="update status_solution set result=2 where id=%d"%RunID
		# print sql
		self.cursor.execute(sql)
		self.conn.commit()
	def SelectSolution(self):
		sql="select * from status_solution where result=1 order by in_date "
		n = self.cursor.execute(sql) 
		# print "查询得到的记录行数:%d" %n
		if n==0:
			return False
		rows=self.cursor.fetchone()  
		# print "查询得到的记录RunID：%d"%rows[0]
		# print rows
		return rows
 	def SelectCode(self,RunID):
 		sql="select * from status_source_code where solution_id= %d" %RunID
 		# print sql
 		m = self.cursor.execute(sql)
 		if m==0:
 			return False
		rows=self.cursor.fetchone()
		return rows
	def Reset(self):
		self.cursor.close()
		self.conn.close()
		self.conn = MySQLdb.connect(user='oj', passwd='oj', db='afoj', use_unicode=True)
		self.cursor = self.conn.cursor()
		self.cursor.execute("set names utf8")
		self.conn.commit()
	def Reset_test(self):
		for RunID in range(12):
			sql="update status_solution set result=1 where id=%d"%(RunID+1)
			self.cursor.execute(sql)
			self.conn.commit()

	def SocreAdd(self):
		sql="select * from problemlist_problem  "
		n = self.cursor.execute(sql) 

		if n==0:
			return False
		rows=self.cursor.fetchall() 
		problem_id_list=[]
		for row in rows:
			problem_id_list.append(row[0])
			# print row[0]
		print problem_id_list
		id=1
		for item in problem_id_list:
			sql="insert problemlist_score (id,file_name,score,problem_id) values(%d,%d,%d,%d)" %(id,1,5,item)
			print sql
			id+=1
			self.cursor.execute(sql)
			self.conn.commit()


if __name__=='__main__':
	GTaskMySQL=GetTaskMySQL()
	GTaskMySQL.SocreAdd()