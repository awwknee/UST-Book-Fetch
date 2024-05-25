from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Notebook, Treeview
from PIL import Image, ImageTk

# Login and Account Creation Window

image_path = "book.jpg"
image = Image.open(image_path)
image = image.resize((100, 100))

class Admin:
	def __init__(self, username, password, mw, conn):
		self.window = Tk()
		self.window.geometry('800x600')
		self.window.title("UST Books")

		self._username = username
		self._password = password
		self.mw = mw
		self.conn = conn

		self.courses = [None]

		courses = self.conn.execute("SELECT Name FROM Courses").fetchall()
		for (name) in courses:
			self.courses.append(name[0])

		self.set_frame = Frame(self.window, width=100, height=50)
		self.set_frame.pack(anchor='ne')
		
		self.set_frame.grid_columnconfigure(0, weight=1)
		self.set_frame.grid_columnconfigure(1, weight=1)

		self.logout_label = Button(self.set_frame, text="Logout", command=self.logout)
		self.logout_label.grid(column=0, row=0)

		image_path = "book.jpg"
		image = Image.open(image_path)
		image = image.resize((100, 100))
		self.book_image = ImageTk.PhotoImage(image)
		self.book_label = Label(self.window, image=self.book_image, height=100, width=100, border=0)
		self.book_label.pack()

		self.title_label = Label(self.window, text="UST Books", font=("Arial", 20, "bold"), background='white')
		self.title_label.pack()

		self.login_label = Label(self.window, text="Administrator", font=("Arial", 20, "bold"), background='white', pady=50)
		self.login_label.pack()

		self.frame = Frame(self.window, background='white')
		self.frame.pack(fill=BOTH, expand=True)

		self.frame.columnconfigure(0, weight=1)
		self.frame.columnconfigure(1, weight=1)
		self.frame.rowconfigure(0, weight=1)
		self.frame.rowconfigure(1, weight=1)
		
		self.books = Frame(self.frame, background='white')
		self.books.grid(column=0, row=0, sticky="nsew")

		self.book_label = Label(self.books, text="Create new Book", font=("Arial", 20, "bold"), background='white')
		self.book_label.pack()

		self.book_title_label = Label(self.books, text="Book Title", background='white')
		self.book_title_label.pack()

		self.book_title = Entry(self.books, background='white')
		self.book_title.pack()

		self.book_isbn_label = Label(self.books, text="Book ISBN", background='white')
		self.book_isbn_label.pack()

		self.book_isbn = Entry(self.books, background='white')
		self.book_isbn.pack()

		self.book_isbn_label = Label(self.books, text="Course Name", background='white')
		self.book_isbn_label.pack()

		self.book_course = Combobox(self.books, values=self.courses, background='white')
		self.book_course.set("None")
		self.book_course.pack()

		self.submit = Button(self.books, text="Add Book", command=self.createBook)
		self.submit.pack(pady=2)
		
		self.university = Frame(self.frame, background='white')
		self.university.grid(column=1, row=0, sticky="nsew")
		
		self.university_label = Label(self.university, text="Create new Unversity", font=("Arial", 20, "bold"), background='white')
		self.university_label.pack()

		self.university_title_label = Label(self.university, text="University Name", background='white')
		self.university_title_label.pack()

		self.university_title = Entry(self.university, background='white')
		self.university_title.pack()

		self.submit = Button(self.university, text="Add University", command=self.addUni)
		self.submit.pack(pady=2)

		self.submitDepart = Button(self.university, text="Add Departments", command=self.addDep)
		self.submitDepart.pack(pady=2)

		self.window.configure(background='white')
		self.window.mainloop()

	def logout(self):
		self.window.destroy()
		self.conn.close()
		self.mw()

	def createBook(self):
		title = self.book_title.get()
		#isbn = self.book_isbn.get()
		course = self.book_course.get()

		cursor = self.conn.execute("INSERT INTO Books (Title) Values ('{}')".format(title))
		self.conn.commit()

		if course != 'None':
			course = self.conn.execute("SELECT CourseID From Courses WHERE Name = '{}'".format(course)).fetchone()[0]
			self.conn.execute("INSERT INTO CourseReadings (ISBN, CourseID) Values ('{}', '{}')".format(cursor.lastrowid, course))
			self.conn.commit()
			messagebox.showinfo("UST Book: Book Added", "The book was succesfully added.")
		

	def addUni(self):
		uni = self.university_title.get()
		self.conn.execute("INSERT INTO Universities (Name) Values ('{}')".format(uni))
		self.conn.commit()

		result = messagebox.askyesno("Create new departments", "The university was created successfully. Would you like to create departments now?")
		if result == True:
			self.window.destroy()
			AdminDepartment(self._username, self._password, self.mw, self.conn)

	def addDep(self):
		self.window.destroy()
		AdminDepartment(self._username, self._password, self.mw, self.conn)

class AdminDepartment:
	def __init__(self, username, password, mw, conn):
		self.window = Tk()
		self.window.geometry('800x600')
		self.window.title("UST Books")

		self._username = username
		self._password = password
		self.mw = mw
		self.conn = conn

		unis = self.conn.execute("SELECT Name FROM Universities").fetchall()
		departments = self.conn.execute("SELECT Name FROM Departments").fetchall()
		
		self.unis = []
		self.departments = []

		for (name) in unis:
			if name[0] != None:
				self.unis.append(name[0])

		for (name) in departments:
			self.departments.append(name[0])

		self.set_frame = Frame(self.window, width=100, height=50)
		self.set_frame.pack(anchor='ne')
		
		self.set_frame.grid_columnconfigure(0, weight=1)
		self.set_frame.grid_columnconfigure(1, weight=1)

		self.univ_label = Button(self.set_frame, text="Back", command=self.back)
		self.univ_label.grid(column=0, row=0)
		self.logout_label = Button(self.set_frame, text="Logout", command=self.logout)
		self.logout_label.grid(column=1, row=0)

		self.book_image = ImageTk.PhotoImage(image)
		self.book_label = Label(self.window, image=self.book_image, height=100, width=100, border=0)
		self.book_label.pack()

		self.title_label = Label(self.window, text="UST Books", font=("Arial", 20, "bold"), background='white')
		self.title_label.pack()

		self.login_label = Label(self.window, text="Administrator", font=("Arial", 20, "bold"), background='white', pady=50)
		self.login_label.pack()

		self.frame = Frame(self.window, background='white')
		self.frame.pack(fill=BOTH, expand=True)

		self.frame.columnconfigure(0, weight=1)
		self.frame.columnconfigure(1, weight=1)
		
		self.department = Frame(self.frame, background='white')
		self.department.grid(column=0, row=0, sticky="nsew")

		self.department_label = Label(self.department, text="Create new Department", font=("Arial", 20, "bold"), background='white')
		self.department_label.pack()

		self.uni_name_label = Label(self.department, text="University Name", background='white')
		self.uni_name_label.pack()

		self.uni_name = Combobox(self.department, values=self.unis, background='white', state="readonly")
		self.uni_name.pack()

		self.department_title_label = Label(self.department, text="Department Name", background='white')
		self.department_title_label.pack()

		self.department_title = Entry(self.department, background='white')
		self.department_title.pack()

		self.submit = Button(self.department, text="Add Department", command=self.addDepart)
		self.submit.pack(pady=2)

		self.courses = Frame(self.frame, background='white')
		self.courses.grid(column=1, row=0, sticky="nsew")
		
		self.courses_label = Label(self.courses, text="Create new Course", font=("Arial", 20, "bold"), background='white')
		self.courses_label.pack()

		self.courses_uni_label = Label(self.courses, text="University Name", background='white')
		self.courses_uni_label.pack()

		self.courses_uni = Combobox(self.courses, values=self.unis)
		self.courses_uni.bind("<<ComboboxSelected>>", self.on_uni_change)
		self.courses_uni.pack()

		self.courses_depart_label = Label(self.courses, text="Department Name", background='white')
		self.courses_depart_label.pack()

		self.courses_depart = Combobox(self.courses, values=self.departments)
		self.courses_depart.pack()

		self.courses_title_label = Label(self.courses, text="Course Name", background='white')
		self.courses_title_label.pack()

		self.courses_title = Entry(self.courses, background='white')
		self.courses_title.pack()

		self.courses_year_label = Label(self.courses, text="Course Year", background='white')
		self.courses_year_label.pack()

		self.courses_year = Entry(self.courses, background='white')
		self.courses_year.pack()

		self.courses_semester_label = Label(self.courses, text="Course Semester", background='white')
		self.courses_semester_label.pack()

		self.courses_semester = Entry(self.courses, background='white')
		self.courses_semester.pack()

		self.submit = Button(self.courses, text="Add Course", command=self.addCourse)
		self.submit.pack(pady=2)

		self.window.configure(background='white')
		self.window.mainloop()

	def logout(self):
		self.window.destroy()
		self.conn.close()
		self.mw()

	def back(self):
		self.window.destroy()
		Admin(self._username, self._password, self.mw, self.conn)


	def on_uni_change(self, e):
				uni = self.conn.execute("SELECT UniversityID FROM Universities WHERE Name = '{}'".format(self.courses_uni.get())).fetchone()[0]

				departments = self.conn.execute("SELECT Name FROM Departments Where UniversityID = '{}'".format(uni)).fetchall()
				self.departments.clear()
				for (name) in departments:
					self.departments.append(name[0])
				self.courses_depart.set('')
				self.courses_depart['values'] = self.departments

	
	def addDepart(self):
		dep = self.department_title.get()
		uni = self.conn.execute("SELECT UniversityID FROM Universities WHERE Name = '{}'".format(self.uni_name.get())).fetchone()[0]

		if (dep != None):
			self.conn.execute("INSERT INTO Departments (UniversityID, Name) Values ('{}', '{}')".format(uni, dep))
			self.conn.commit()
			messagebox.showinfo("UST Book: Department Added", "The department was succesfully added.")



	def addCourse(self):
		uni = self.courses_uni.get()
		dep = self.courses_depart.get()

		uniID = self.conn.execute("SELECT UniversityID FROM Universities WHERE Name = '{}'".format(uni)).fetchone()[0]
		depID = self.conn.execute("SELECT DepartmentID FROM Departments WHERE Name = '{}' AND UniversityID = '{}'".format(dep, uniID)).fetchone()[0]

		name = self.courses_title.get()
		year = self.courses_year.get()
		semester = self.courses_semester.get()

		self.conn.execute("INSERT INTO Courses (UniversityID, DepartmentID, Name, Year, Semester) Values ('{}','{}','{}','{}','{}')".format(uniID, depID, name, year, semester))
		self.conn.commit()
		messagebox.showinfo("UST Book: Course Added", "The course was succesfully added.")




		


