from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Notebook
from PIL import Image, ImageTk
from student import Student


# Login and Account Creation Window

image_path = "book.jpg"
image = Image.open(image_path)
image = image.resize((100, 100))

class StudentLogin:
	def __init__(self, username, password, MainWindow, connection):
		self.window = Tk()
		self.window.geometry('800x600')
		self.window.title("UST Books")

		self.connection = connection

		self._username = username
		self._password = password

		self._mainwindow = MainWindow

		self.book_image = ImageTk.PhotoImage(image)
		self.book_label = Label(self.window, image=self.book_image, height=100, width=100, border=0)
		self.book_label.pack();

		self.title_label = Label(self.window, text="UST Books", font=("Arial", 20, "bold"), background='white')
		self.title_label.pack();

		self.login_label = Label(self.window, text="Student Login", font=("Arial", 20, "bold"), background='white', pady=50)
		self.login_label.pack();

		self.login_frame = Frame(self.window, width=200, height=200, background='white')
		self.login_frame.pack();

		self.login_frame.columnconfigure(0, weight=1)
		self.login_frame.columnconfigure(1, weight=1)

		self.username = Entry(self.login_frame, background='white')
		if self._username:
			self.username.insert(0, self._username)
		else:
			self.username.insert(0, "Email")
		self.username.bind("<FocusIn>", self.on_entry_click)
		self.username.bind("<FocusOut>", self.on_entry_leave)
		self.username.config(fg="grey")  # Change text color back to grey
		self.username.grid(row=0, column=0)
		self.password = Entry(self.login_frame, background='white')
		self.password.bind("<FocusIn>", self.on_entry_click)
		self.password.bind("<FocusOut>", self.on_entry_leave)
		if self._password:
			self.password.insert(0, self._password)
		else:
			self.password.insert(0, "Password")
		self.password.config(fg="grey")  # Change text color back to grey
		self.password.grid(row=1, column=0)


		self.login = Button(self.login_frame, text="Login", width=50, command=self.studLogin)
		self.login.grid(row=2, column=0)

		self.text_label = Label(self.window, text="New to UST Books? Sign up!")
		self.text_label.pack()
		self.text_label.bind("<Button-1>", self.new_account)
		
		self.window.config(background='white')
		self.window.mainloop()

	def on_entry_click(self, event):
		if event.widget.get() == "Email":
				self.username.delete(0, "end")
				self.username.config(fg="black")  # Change text color when the user starts typing
		if event.widget.get() == "Password":
				self.password.delete(0, "end")
				self.password.config(fg="black")  # Change text color when the user starts typing

	def on_entry_leave(self, event):
		if event.widget.get() == "" and event.widget == self.username:
				event.widget.insert(0, "Email")
				self.username.config(fg="grey")  # Change text color back to grey
		if event.widget.get() == "" and event.widget == self.password:
				self.password.insert(0, "Password")
				self.password.config(fg="grey")  # Change text color back to grey

	def new_account(self, e):
		mw = self._mainwindow
		self.window.destroy()
		StudentSignup(mw, self.connection)

	def studLogin(self):
		mw = self._mainwindow
		conn = self.connection

		try:
			row = self.connection.execute("SELECT Email_Address, Password FROM Student_users WHERE Email_Address = '" + self.username.get() + "'").fetchone()

		except:
			messagebox.showerror('Login Error','There is no account associated with: ' + self.username.get())
		else:
			if row == None:
				messagebox.showerror('Login Error','There is no account associated with: ' + self.username.get())
			else:
				self.window.destroy()
				Student(row[0], row[1], mw, conn)




		

class StudentSignup:
	def __init__(self, mainwindow, conn):
		self.window = Tk()
		self.window.geometry('800x600')
		self.window.title("UST Books")

		self._mainwindow = mainwindow

		self.conn = conn;

		self.uni = [];

		rows = self.conn.execute('SELECT Name FROM Universities').fetchall()
		for name in rows:
			self.uni.append(name[0])

		self.book_image = ImageTk.PhotoImage(image)
		self.book_label = Label(self.window, image=self.book_image, height=100, width=100, border=0)
		self.book_label.pack();

		self.title_label = Label(self.window, text="UST Books", font=("Arial", 20, "bold"), background='white')
		self.title_label.pack();

		self.login_label = Label(self.window, text="Student Sign Up", font=("Arial", 20, "bold"), background='white', pady=50)
		self.login_label.pack();

		self.login_frame = Frame(self.window, width=200, height=200, background='white')
		self.login_frame.pack();

		self.login_frame.columnconfigure(0, weight=1)
		self.login_frame.columnconfigure(1, weight=1)

		self.username = Entry(self.login_frame, background='white')
		self.username.insert(0, "Email")
		self.username.bind("<FocusIn>", self.on_entry_click)
		self.username.bind("<FocusOut>", self.on_entry_leave)
		self.username.config(fg="grey")  # Change text color back to grey
		self.username.grid(row=0, column=0)

		self.password = Entry(self.login_frame, background='white')
		self.password.bind("<FocusIn>", self.on_entry_click)
		self.password.bind("<FocusOut>", self.on_entry_leave)
		self.password.insert(0, "Password")
		self.password.config(fg="grey")  # Change text color back to grey
		self.password.grid(row=1, column=0)

		self.first_name = Entry(self.login_frame, background='white')
		self.first_name.bind("<FocusIn>", self.on_entry_click)
		self.first_name.bind("<FocusOut>", self.on_entry_leave)
		self.first_name.insert(0, "First Name")
		self.first_name.config(fg="grey")  # Change text color back to grey
		self.first_name.grid(row=2, column=0)

		self.last_name = Entry(self.login_frame, background='white')
		self.last_name.bind("<FocusIn>", self.on_entry_click)
		self.last_name.bind("<FocusOut>", self.on_entry_leave)
		self.last_name.insert(0, "Last Name")
		self.last_name.config(fg="grey")  # Change text color back to grey
		self.last_name.grid(row=3, column=0)

		self.address = Entry(self.login_frame, background='white')
		self.address.bind("<FocusIn>", self.on_entry_click)
		self.address.bind("<FocusOut>", self.on_entry_leave)
		self.address.insert(0, "Address")
		self.address.config(fg="grey")  # Change text color back to grey
		self.address.grid(row=4, column=0)

		self.telephone = Entry(self.login_frame, background='white')
		self.telephone.bind("<FocusIn>", self.on_entry_click)
		self.telephone.bind("<FocusOut>", self.on_entry_leave)
		self.telephone.insert(0, "Telephone")
		self.telephone.config(fg="grey")  # Change text color back to grey
		self.telephone.grid(row=5, column=0)

		self.birth_date = Entry(self.login_frame, background='white')
		self.birth_date.bind("<FocusIn>", self.on_entry_click)
		self.birth_date.bind("<FocusOut>", self.on_entry_leave)
		self.birth_date.insert(0, "Birth Date")
		self.birth_date.config(fg="grey")  # Change text color back to grey
		self.birth_date.grid(row=6, column=0)

		self.university_label = Label(self.login_frame, text="University", background='white')
		self.university_label.grid(row=7, column=0)

		self.university = Combobox(self.login_frame, background='white', values=self.uni, state="readonly")
		self.university.grid(row=8, column=0)

		self.status_label = Label(self.login_frame, text="Status", background='white')
		self.status_label.grid(row=9, column=0)

		self.status = Combobox(self.login_frame, background='white', values=["UnderGrad","Grad"], state="readonly")
		self.status.set("UnderGrad")
		self.status.grid(row=10, column=0)

		self.year_label = Label(self.login_frame, text="Year", background='white')
		self.year_label.grid(row=11, column=0)

		self.year = Combobox(self.login_frame, background='white', values=[1,2,3,4,5,6,7,8], state="readonly")
		self.year.set("1");
		self.year.grid(row=12, column=0)

		self.login = Button(self.login_frame, text="Sign Up", width=50, command=self.signup)
		self.login.grid(row=13, column=0)
		
		self.window.config(background='white')
		self.window.mainloop()

	def on_entry_click(self, event):
		if event.widget.get() == "Email":
				self.username.delete(0, "end")
				self.username.config(fg="black")  # Change text color when the user starts typing
		if event.widget.get() == "Password":
				self.password.delete(0, "end")
				self.password.config(fg="black")  # Change text color when the user starts typing
		if event.widget.get() == "First Name":
				self.first_name.delete(0, "end")
				self.first_name.config(fg="black")  # Change text color when the user starts typing
		if event.widget.get() == "Last Name":
				self.last_name.delete(0, "end")
				self.last_name.config(fg="black")  # Change text color when the user starts typing
		if event.widget.get() == "Address":
				self.address.delete(0, "end")
				self.address.config(fg="black")  # Change text color when the user starts typing
		if event.widget.get() == "Telephone":
				self.telephone.delete(0, "end")
				self.telephone.config(fg="black")  # Change text color when the user starts typing
		if event.widget.get() == "Birth Date":
				self.birth_date.delete(0, "end")
				self.birth_date.config(fg="black")  # Change text color when the user starts typing

	def on_entry_leave(self, event):
		if event.widget.get() == "" and event.widget == self.username:
				event.widget.insert(0, "Email")
				self.username.config(fg="grey")  # Change text color back to grey
		if event.widget.get() == "" and event.widget == self.password:
				self.password.insert(0, "Password")
				self.password.config(fg="grey")  # Change text color back to grey
		if event.widget.get() == "" and event.widget == self.first_name:
				self.first_name.insert(0, "First Name")
				self.first_name.config(fg="grey")  # Change text color back to grey
		if event.widget.get() == "" and event.widget == self.last_name:
				self.last_name.insert(0, "Last Name")
				self.last_name.config(fg="grey")  # Change text color back to grey
		if event.widget.get() == "" and event.widget == self.address:
				self.address.insert(0, "Address")
				self.address.config(fg="grey")  # Change text color back to grey
		if event.widget.get() == "" and event.widget == self.telephone:
				self.telephone.insert(0, "Telephone")
				self.telephone.config(fg="grey")  # Change text color back to grey
		if event.widget.get() == "" and event.widget == self.birth_date:
				self.birth_date.insert(0, "Birth Date")
				self.birth_date.config(fg="grey")  # Change text color back to grey

	def signup(self):
		username = self.username.get()
		password = self.password.get()
		first_name = self.first_name.get()
		last_name = self.last_name.get()
		address = self.address.get()
		telephone = self.telephone.get()
		birth_date = self.birth_date.get()
		uni = self.university.get()
		status = self.status.get()
		year = self.year.get()

		mw = self._mainwindow

		uni = self.conn.execute("SELECT UniversityID FROM Universities WHERE Name = '{}'".format(uni)).fetchone()[0]
		self.conn.execute("INSERT INTO Student_users (Email_Address, Password, First_Name, Last_Name, Address, Phone_Number, Birth_Date, UniversityID, Status, Year) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(username, password, first_name, last_name, address, telephone, birth_date, uni, status, year))
		self.conn.commit()
		self.window.destroy()
		StudentLogin(username, password, mw, self.conn)

	