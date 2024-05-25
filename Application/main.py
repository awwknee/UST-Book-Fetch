import sqlite3
from tkinter import *
from tkinter.ttk import Notebook
from PIL import Image, ImageTk

from student_login import StudentLogin
from employee_login import EmployeeLogin

# Login and Account Creation Window

image_path = "book.jpg"
image = Image.open(image_path)
image = image.resize((100, 100))

class MainWindow:
	def __init__(self):
		self.window = Tk()
		self.window.geometry('800x600')
		self.window.title("UST Books")

		self._connection = sqlite3.connect('./ustbooks.db');
		self._connection.execute("PRAGMA foreign_keys = ON")
		self._connection.commit()

		# Code To Create Database
		#with open("./scripts/create_tables.sql", "r") as f:
			#self._connection.executescript(f.read())

		#Code to Import Data
		#with open("./scripts/insert_data.sql", "r") as f:
			#self._connection.executescript(f.read())
		
		# Code to Add Fake Users For Testing
		# Just uncomment and run file
		#self._connection.execute("INSERT INTO SUPER_ADMINISTRATORS (First_Name) Values ('sadmin')")
		#self._connection.commit()

		#self._connection.execute("INSERT INTO ADMINISTRATORS (First_Name) Values ('admin')")
		#self._connection.commit()

		#self._connection.execute("INSERT INTO Customer_support_users (First_Name) Values ('cs')")
		#self._connection.commit()

		self.book_image = ImageTk.PhotoImage(image)
		self.book_label = Label(self.window, image=self.book_image, height=100, width=100, border=0)
		self.book_label.pack();

		self.title_label = Label(self.window, text="UST Books", font=("Arial", 20, "bold"), background='white')
		self.title_label.pack();

		self.login_label = Label(self.window, text="Login", font=("Arial", 20, "bold"), background='white', pady=50)
		self.login_label.pack();

		self.login_frame = Frame(self.window, width=200, height=200)
		self.login_frame.pack();

		self.login_frame.columnconfigure(0, weight=1)
		self.login_frame.columnconfigure(1, weight=1)

		self.button1 = Button(self.login_frame, text="Student", width=50, command=self.openStudentLogin)
		self.button2 = Button(self.login_frame, text="Employee", width=50, command=self.openEmployeeLogin)

		self.button1.grid(row=0, column=0)
		self.button2.grid(row=0, column=1)

		self.window.config(background='white')
		self.window.mainloop()

	def openStudentLogin(self):
		self.window.destroy()

		StudentLogin(None, None, MainWindow, self._connection)
	def openEmployeeLogin(self):
		self.window.destroy()
		employeelogin()
		EmployeeLogin(None, None, MainWindow, self._connection)



main = MainWindow()


	