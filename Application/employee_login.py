from tkinter import *
from tkinter.ttk import Notebook
from PIL import Image, ImageTk

from employee import Employee
from admin import Admin
from superadmin import SuperAdmin


# Login and Account Creation Window

image_path = "book.jpg"
image = Image.open(image_path)
image = image.resize((100, 100))

class EmployeeLogin:
	def __init__(self, username, password, mw, conn):
		self.window = Tk()
		self.window.geometry('800x600')
		self.window.title("UST Books")

		self._username = username;
		self._password = password;

		self.mw = mw;
		self.conn = conn;


		self.book_image = ImageTk.PhotoImage(image)
		self.book_label = Label(self.window, image=self.book_image, height=100, width=100, border=0)
		self.book_label.pack();

		self.title_label = Label(self.window, text="UST Books", font=("Arial", 20, "bold"), background='white')
		self.title_label.pack();

		self.login_label = Label(self.window, text="Employee Login", font=("Arial", 20, "bold"), background='white', pady=50)
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


		self.login = Button(self.login_frame, text="Login", width=50, command=self.emp_login)
		self.login.grid(row=2, column=0)
		
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

	def emp_login(self):
		username = self.username.get()

		rows = self.conn.execute("SELECT First_Name, Email_Address, 1 FROM Customer_support_users UNION SELECT First_Name, Email_Address, 2 FROM Administrators UNION SELECT First_Name, Email_Address, 3 FROM Super_administrators").fetchall()
		print(rows)
		
		for (Name, Email, Type) in rows:
			if Name == username:
				self.window.destroy()
				if Type == 1:
					Employee(username, self._password, self.mw, self.conn)
				elif Type == 2:
					Admin(username, self._password, self.mw, self.conn)
				elif Type == 3:
					SuperAdmin(username, self._password, self.mw, self.conn)

				

	