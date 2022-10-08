import sqlite3


# create database file
class Database:

	def __init__(self):

		self.conn = sqlite3.connect("todo.db")
		self.cursor = self.conn.cursor()

	# create table 
	def db_table(self):

		self.cursor.execute("CREATE TABLE IF NOT EXISTS taskTodo(task TEXT UNIQUE, task_status TEXT, task_due_date DATE)")

	def add_db(self, task, task_status, task_due_date):

		self.cursor.execute("INSERT INTO taskTodo(task, task_status, task_due_date) VALUES(?, ?, ?) ", (task, task_status, task_due_date))
		self.conn.commit()

	def read_db(self):
		
		self.cursor.execute("SELECT * FROM taskTodo")
		return self.cursor.fetchall()

	def unique_task(self):
		
		self.cursor.execute("SELECT DISTINCT task FROM taskTodo")
		return self.cursor.fetchall()

	def get_task(self, task):

		self.cursor.execute("SELECT * FROM taskTodo WHERE task='{}'".format(task))
		return self.cursor.fetchall()

	def update_db(self, new_task,new_task_status,new_task_date,task,task_status,task_due_date):
		self.cursor.execute("UPDATE taskTodo SET task =?,task_status=?,task_due_date=? WHERE task=? and task_status=? and task_due_date=? ",(new_task,new_task_status,new_task_date,task,task_status,task_due_date))
		self.conn.commit()
		return self.cursor.fetchall()

	def detele_db(self, task):

		self.cursor.execute("DELETE FROM taskTodo WHERE task='{}'".format(task))
		self.conn.commit()
		self.cursor.fetchall()


if __name__ == '__main__':
	db = Database()
	db.update_db("Hahah", "Testing", "2022-10-10", "Dont do that bro", "Doing", "2022-10-10")
