import time
from datetime import datetime
import asyncio
from sqlite3 import OperationalError

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
from PIL import Image
# import typer
from rich.console import Console

from db import Database
# from db.Database import read_db, add_db, update_db, detele_db

# setting the layout attribute
st.set_page_config(layout="wide")

def main():

	

	menu = [
	"Create",
	"Read",
	"Update",
	"Delete",
	"About Me"
	]

	title = st.title("Todo App with streamlit")
	side_title = st.sidebar.title("Rich Feature Selection")
	choice = st.sidebar.selectbox("Freatures", menu)

	db_actions = Database()
	db_actions.db_table()

	if choice == "Create":
		st.subheader("Add Items")

		# task asctions
		task = st.text_area("Task to do")

		# layout
		col1, col2 = st.columns(2)
		with col1:
			task_status = st.selectbox("Status", ["Todo", "Doing", "Testing", "Done"])
		with col2:
			task_due_date = st.date_input("Due date")

		if st.button("Add task"):

			try:
				add_time = time.localtime()
				db_actions.add_db(task, task_status, task_due_date)
				st.success("Task added on {}".format(time.strftime('%Y-%m-%d %A', add_time)))
			
			except:
				st.error("Task already exists! Try updating the task")

		with st.expander("All tasks"):
			st.subheader("All tasks")
			all_tasks = db_actions.read_db()
			df = pd.DataFrame(all_tasks, columns=["Task", "Status", "Due Date"])
			st.dataframe(df)

	elif choice == "Read":

		st.subheader("Read Items")
		all_tasks = db_actions.read_db()
		df = pd.DataFrame(all_tasks, columns=["Task", "Status", "Due Date"])
		
		with st.expander("All tasks"):
			st.dataframe(df)

		with st.expander("Status"):
			task_df = df["Status"].value_counts().to_frame()
			task_df = task_df.reset_index()
			st.dataframe(task_df)

		with st.expander("Graph representation"):
			data_plot = px.pie(task_df, names="index", values="Status")
			st.plotly_chart(data_plot)


	elif choice == "Update":

		def iter_task():
			list_of_tasks = []

			try:

				for i in db_actions.unique_task():
					for val in i:
						list_of_tasks.append(val)

				return list_of_tasks

			except:
				return list_of_tasks.append("No tasks")

		st.subheader("Update Items")
		result = db_actions.read_db()
		df = pd.DataFrame(result, columns=["Task", "Status", "Due Date"])

		list_of_tasks = iter_task()

		# st.dataframe(list_of_tasks)
		with st.expander("Current data"):
				st.dataframe(df)
		selected_task = st.selectbox("Choose tasks to update", list_of_tasks)
		selected_result = db_actions.get_task(selected_task)



		if selected_result not in list_of_tasks:
			try:
				task = selected_result[0][0]
				task_status = selected_result[0][1]
				task_due_date = selected_result[0][2]
				# task asctions
				new_task = st.text_area("Update to")

				# layout
				col1, col2 = st.columns(2)
				with col1:
					new_task_status = st.selectbox(f"[{task_status}] to", ["Todo", "Doing", "Testing", "Done"])
				with col2:
					new_task_due_date = st.date_input(f"[{task_due_date}] to")

				if st.button("Update task"):

					try:
						add_time = time.localtime()
						db_actions.update_db(new_task, new_task_status, new_task_due_date, task, task_status, task_due_date)
						st.success("Task added on {}".format(time.strftime('%Y-%m-%d %A', add_time)))
					
					except:
						st.error("Task already exists! Try updating the task")

			except:
				st.error("No tasks to update")

	# deleting a task
	elif choice == "Delete":

		st.subheader("Delete Item")

		all_tasks = db_actions.read_db()

		df = pd.DataFrame(all_tasks, columns=["Task", "Status", "Due Date"])
		

		def iter_task():
			list_of_tasks = []

			try:

				for i in db_actions.unique_task():
					for val in i:
						list_of_tasks.append(val)

				return list_of_tasks

			except:
				return list_of_tasks.append("No tasks")

		list_of_tasks = iter_task()

		# st.dataframe(list_of_tasks)
		selected_task = st.selectbox("Select tasks", list_of_tasks)
		selected_result = db_actions.get_task(selected_task)

		if selected_result not in list_of_tasks:
			try:
				# st.error("No such task!")	
				task = selected_result[0][0]
				task_status = selected_result[0][1]
				task_due_date = selected_result[0][2]

				if st.button("Delete task"):
					# try:
					add_time = time.localtime()
					db_actions.detele_db(task)
					st.error("Task Deleted on {}".format(time.strftime('%Y-%m-%d %A', add_time)))

				st.dataframe(df)

			except:

				st.error("No tasks!")

	elif choice == "About Me":

		title = st.title("Shadrack Meoli")
		# st.subheader("Machine learning engineer, data scientist, backend developer and Quality Assurance automation engineer")

		col1, col2 = st.columns(2)

		with col1:
			image = Image.open("assets/official.jpg")
			st.image(image, width=250, caption="This is me")

		with col2:
			st.write("""
					I am a Machine learning engineer, data scientist, 
				python backend develoer and a Quality Assurance(QA) automation engineer.
				Aspiring to be a lead machine learning engineer with a certificate 
				in data science I have perfected my database administrative skills 
				and working with online servers(AWS and Linode server). 
				I offer four years of experience in Data science and software engineering with excellent skills in
				python, R, databases, javascript and office statistical tools and web development tools and frameworks 
				which should make me a strong candidate for this role. I have strong skills in python programming, 
				relational databases, cloud computing and version control software. 
 				I have grown my skills in problem-solving with real-world tasks and pressure. 
 				I believe my ability to develop robust, scalable code with yielding results.
				""")

		skills = {
			"Tools": ["Python", "AWS", "VueJs", "NodeJS", "Jupyter Notebook", "SQL"],
			"Years Of Experience": ["5 years", "1 year", "2 Years", "3 Years", "4 years", "4 Years"],
			"Ranking": ["Very Good", "Average", "Good", "Good", "Very Good", "Very Good"]
		}

		df = pd.DataFrame(skills)

		st.write("Skill showcase")
		st.dataframe(df)

if __name__ == '__main__':
	main()
	import os
	os.system("streamlit run dash.py")
