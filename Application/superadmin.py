from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Notebook, Treeview
from PIL import Image, ImageTk


# Login and Account Creation Window

image_path = "book.jpg"
image = Image.open(image_path)
image = image.resize((100, 100))

class SuperAdmin:
	def __init__(self, username, password, mw, conn):
		self.window = Tk()
		self.window.geometry('800x650')
		self.window.title("UST Books")

		self._username = username
		self._password = password
		self.mw = mw
		self.conn = conn

		staff = self.conn.execute("SELECT CSEmployeeID, First_Name, 1 FROM Customer_support_users UNION SELECT AEmployeeID, First_Name, 2 FROM Administrators").fetchall()
		self.staff = []

		for (id, name, type) in staff:
			self.staff.append((id, name, type))

		self.set_frame = Frame(self.window, width=100, height=50)
		self.set_frame.pack(anchor='ne')
		
		self.set_frame.grid_columnconfigure(0, weight=1)
		self.set_frame.grid_columnconfigure(1, weight=1)

		self.logout_label = Button(self.set_frame, text="Logout", command=self.logout)
		self.logout_label.grid(column=0, row=0)
			

		self.book_image = ImageTk.PhotoImage(image)
		self.book_label = Label(self.window, image=self.book_image, height=100, width=100, border=0)
		self.book_label.pack()

		self.title_label = Label(self.window, text="UST Books", font=("Arial", 20, "bold"), background='white')
		self.title_label.pack()

		self.login_label = Label(self.window, text="Super Administrator", font=("Arial", 20, "bold"), background='white', pady=50)
		self.login_label.pack()

		self.frame = Frame(self.window, background='white')
		self.frame.pack(fill=BOTH, expand=True)

		self.frame.columnconfigure(0, weight=1)
		self.frame.columnconfigure(1, weight=1)

		self.admin = Frame(self.frame, background='white')
		self.admin.grid(column=0, row=0, sticky="nsew")

		self.admin_label = Label(self.admin, text="Employees",font=("Arial", 20, "bold"), background='white')
		self.admin_label.pack()

		self.admin_tree = Treeview(self.admin, columns=("Id", "Name", "Deactivate"), show="headings")
		self.admin_tree.heading("Id", text="Id")
		self.admin_tree.heading("Name", text="Name")
		self.admin_tree.heading("Deactivate", text="Deactivate")

		self.admin_tree.column("Id", width=100)
		self.admin_tree.column("Name", width=100)
		self.admin_tree.column("Deactivate", width=200)

		for (id, name, type) in self.staff:
			if type == 1:
				self.admin_tree.insert('', 'end', value=(id, name, "Deactivate Employee"))
			else:
				self.admin_tree.insert('', 'end', value=(id, name, "Deactivate Admin"))

		self.admin_tree.pack()

		self.admin_tree.bind("<ButtonRelease-1>", self.tree_click)

		
		self.employees = Frame(self.frame, background='white')
		self.employees.grid(column=1, row=0, sticky="nsew")

		self.employees_label = Label(self.employees, text="Create new Employee", font=("Arial", 20, "bold"), background='white')
		self.employees_label.pack()

		self.ticket_title_label = Label(self.employees, text="Employee Type", background='white')
		self.ticket_title_label.pack()
		
		self.employees_type = Combobox(self.employees, values=("Admin", "Customer Service"))
		self.employees_type.pack()

		self.employees_first_name_label = Label(self.employees, text="Employee First Name", background='white')
		self.employees_first_name_label.pack()

		self.employee_first_name = Entry(self.employees, background='white')
		self.employee_first_name.pack()

		self.employees_last_name_label = Label(self.employees, text="Employee Last Name", background='white')
		self.employees_last_name_label.pack()

		self.employee_last_name = Entry(self.employees, background='white')
		self.employee_last_name.pack()

		self.employees_gender_label = Label(self.employees, text="Employee Gender", background='white')
		self.employees_gender_label.pack()

		self.employee_gender = Combobox(self.employees, background='white', values=["Male", "Female", "Other"], state="readonly")
		self.employee_gender.set("Male")
		self.employee_gender.pack()

		self.employees_ssn_label = Label(self.employees, text="Employee SSN", background='white')
		self.employees_ssn_label.pack()

		self.employee_ssn = Entry(self.employees, background='white')
		self.employee_ssn.pack()

		self.employees_address_label = Label(self.employees, text="Employee Address", background='white')
		self.employees_address_label.pack()

		self.employee_address = Entry(self.employees, background='white')
		self.employee_address.pack()

		self.employees_telephone_label = Label(self.employees, text="Employee Telephone", background='white')
		self.employees_telephone_label.pack()

		self.employee_telephone = Entry(self.employees, background='white')
		self.employee_telephone.pack()

		self.submit = Button(self.employees, text="Add Employee", command=self.create_employee)
		self.submit.pack(pady=2)

		self.window.configure(background='white')
		self.window.mainloop()

	def logout(self):
		self.window.destroy()
		self.conn.close()
		self.mw()

	def tree_click(self, event):
			region = self.admin_tree.identify("region", event.x, event.y)

			if region == "cell":
				column = self.admin_tree.identify_column(event.x)
				if column == "#3":  # Check if the clicked column is the "Age" column
					item_id = self.admin_tree.identify_row(event.y)
					item_values = self.admin_tree.item(item_id, "values")
					self.admin_tree.delete(item_id)
					id = item_values[0]
					if item_values[2] == "Deactivate Employee":
						self.conn.execute("UPDATE Trouble_Tickets SET Status='new' WHERE CSEmployeeID = '{}'".format(id))
						self.conn.commit()
						self.conn.execute("DELETE FROM Customer_support_users WHERE CSEmployeeID = '{}'".format(id))
						self.conn.commit()
					else:
						self.conn.execute("UPDATE Trouble_Tickets SET Status='new' WHERE AEmployeeID = '{}'".format(id))
						self.conn.commit()
						self.conn.execute("DELETE FROM Administrators WHERE AEmployeeID = '{}'".format(id))
						self.conn.commit()

	def create_employee(self):
		type = self.employees_type.get()
		first_name = self.employee_first_name.get()
		last_name = self.employee_last_name.get()
		gender = self.employee_gender.get()
		ssn = self.employee_ssn.get()
		address = self.employee_address.get()
		phone = self.employee_telephone.get()

		if type == "Admin":
			self.conn.execute("INSERT INTO Administrators (First_Name, Last_Name, Gender, SSN, Address, Phone_Number) Values ('{}', '{}', '{}', '{}', '{}', '{}')".format(first_name, last_name, gender, ssn, address, phone))
			self.conn.commit()
			messagebox.showinfo("UST Book: Admin user added", "The admin user was succesfully added.")
		else:
			self.conn.execute("INSERT INTO Customer_support_users (First_Name, Last_Name, Gender, SSN, Address, Phone_Number) Values ('{}', '{}', '{}', '{}', '{}', '{}')".format(first_name, last_name, gender, ssn, address, phone))
			self.conn.commit()
			messagebox.showinfo("UST Book: Customer Support User Added", "The customer support user was succesfully added.")

