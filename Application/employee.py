from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Notebook, Treeview
from PIL import Image, ImageTk


# Login and Account Creation Window

image_path = "book.jpg"
image = Image.open(image_path)
image = image.resize((100, 100))

class Employee:
	def __init__(self, username, password, mw, conn):
		self.window = Tk()
		self.window.geometry('800x600')
		self.window.title("UST Books")

		self._username = username
		self._password = password
		self.mw = mw
		self.conn = conn

		self._orders = self.conn.execute("SELECT OrderID, StudentID FROM Orders WHERE Fulfilled_Date IS NULL AND Created_Date IS NOT NULL").fetchall()
		self._admins = []

		self.csID = self.conn.execute("SELECT CSEmployeeID FROM Customer_support_users WHERE First_Name = '{}'".format(self._username)).fetchone()[0]

		rows = self.conn.execute("SELECT First_Name FROM Administrators").fetchall()
		for name in rows:
			self._admins.append(name[0])


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

		self.login_label = Label(self.window, text="User Support", font=("Arial", 20, "bold"), background='white', pady=50)
		self.login_label.pack()

		self.frame = Frame(self.window, background='white')
		self.frame.pack(fill=BOTH, expand=True)

		self.frame.columnconfigure(0, weight=1)
		self.frame.columnconfigure(1, weight=1)

		self.orders = Frame(self.frame, background='white')
		self.orders.grid(column=0, row=0, sticky="nsew")

		self.order_label = Label(self.orders, text="Ongoing Orders",font=("Arial", 20, "bold"), background='white')
		self.order_label.pack()

		self.order_tree = Treeview(self.orders, columns=("Id", "Student Id", "Cancel"), show="headings")
		self.order_tree.heading("Id", text="Order Id")
		self.order_tree.heading("Student Id", text="Student Id")
		self.order_tree.heading("Cancel", text="Cancel")

		self.order_tree.column("Id", width=200)
		self.order_tree.column("Student Id", width=100)
		self.order_tree.column("Cancel", width=100)


		for order in self._orders:
			self.order_tree.insert('', 'end', values=(order[0], order[1], "Cancel Order"))

		self.order_tree.pack()

		self.order_tree.bind("<ButtonRelease-1>", self.tree_click)

		
		self.tickets = Frame(self.frame, background='white')
		self.tickets.grid(column=1, row=0, sticky="nsew")


		self.tickets_label = Label(self.tickets, text="Create new ticket", font=("Arial", 20, "bold"), background='white')
		self.tickets_label.pack()

		self.ticket_title_label = Label(self.tickets, text="Ticket Title", background='white')
		self.ticket_title_label.pack()

		self.tickets_title = Entry(self.tickets, text="Title of Ticket", background='white')
		self.tickets_title.pack()

		self.ticket_type_label = Label(self.tickets, text="Ticket Type", background='white')
		self.ticket_type_label.pack()

		self.ticket_type = Combobox(self.tickets, values=['User Profile', 'Products', 'Cart', 'Orders', 'Other'], background='white', state="readonly")
		self.ticket_type.pack()

		self.ticket_desc_label = Label(self.tickets, text="Ticket Description", background='white')
		self.ticket_desc_label.pack()

		self.ticket_desc = Text(self.tickets, background='white', height=3, width=30)
		self.ticket_desc.pack()

		self.student_title_label = Label(self.tickets, text="Student ID", background='white')
		self.student_title_label.pack()

		self.student_id = Entry(self.tickets, background='white')
		self.student_id.pack()

		self.admins_label = Label(self.tickets, text="Assign Admin", background='white')
		self.admins_label.pack()

		self.admins = Combobox(self.tickets, values=self._admins)
		self.admins.pack()

		self.submit = Button(self.tickets, text="Submit Ticket", command=self.create_ticket)
		self.submit.pack(pady=2)

		self.window.configure(background='white')
		self.window.mainloop()

	def logout(self):
		self.window.destroy()
		self.conn.close()
		self.mw()

	def tree_click(self, event):
			region = self.order_tree.identify("region", event.x, event.y)

			if region == "cell":
				column = self.order_tree.identify_column(event.x)
				if column == "#3":  # Check if the clicked column is the "Age" column
					item_id = self.order_tree.identify_row(event.y)
					orderId = self.order_tree.item(item_id, "values")[0]

					self.order_tree.delete(item_id)

					self.conn.execute("DELETE FROM Orders WHERE OrderID = '{}'".format(orderId))
					self.conn.commit()

					self.conn.execute("DELETE FROM OrderBooks Where OrderID = '{}'".format(orderId))
					self.conn.commit()

	def create_ticket(self):
		title = self.tickets_title.get()
		desc = self.ticket_desc.get('1.0', END).replace("'", "''")
		type = self.ticket_type.get()
		student = self.student_id.get()
		admin = self.admins.get()

		if (admin != "None"):
			admin = self.conn.execute("SELECT AEmployeeID FROM Administrators WHERE First_Name = '{}'".format(admin)).fetchone()[0]

			self.conn.execute("INSERT INTO Trouble_Tickets (Category, Date_Logged, StudentID, AEmployeeID, CSEmployeeID, Title, Problem_Description, Status) Values ('{}', CURRENT_DATE, '{}', '{}', '{}', '{}', '{}', '{}')".format(''.join(type.lower().split()), student, admin, self.csID, title, desc, "new"))
			self.conn.commit()
			messagebox.showinfo("UST Books: Ticket Request", "A ticket has been successfully submitted!")
		else:
			messagebox.showerror("UST Books: Ticket Error", "You must select an admin!")
			
		

		
