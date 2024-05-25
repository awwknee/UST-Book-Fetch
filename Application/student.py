from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Notebook, Treeview
from PIL import Image, ImageTk


image_path = "book.jpg"
image = Image.open(image_path)
image = image.resize((100, 100))

class Student:
	def __init__(self, username, password, mainwindow, connection):
		self.window = Tk()
		self.window.geometry('800x600')
		self.window.title("UST Books")

		self._connection = connection
		self._username = username
		self._password = password

		self._mainwindow = mainwindow;

		self.set_frame = Frame(self.window, width=100, height=50)
		self.set_frame.pack(anchor='ne')

		self.set_frame.grid_columnconfigure(0, weight=1)
		self.set_frame.grid_columnconfigure(1, weight=1)
		self.set_frame.grid_columnconfigure(2, weight=1)

		self.cart_label = Button(self.set_frame, text="Cart", command=self.openCart)
		self.logout_label = Button(self.set_frame, text="Logout", command=self.logout)
		self.orders = Button(self.set_frame, text="Ongoing Orders", command=self.ongoingOrders)
		self.cart_label.grid(column=0, row=0)
		self.logout_label.grid(column=2, row=0)
		self.orders.grid(column=1, row=0)


		cartId = self._connection.execute("SELECT CartID FROM Student_users WHERE Email_Address = '{}'".format(self._username)).fetchone()[0]
		self.cartId = cartId

		if cartId == None:
			cursor = self._connection.execute("INSERT INTO Carts (Created_Date, Modified_Date) Values (CURRENT_DATE, CURRENT_DATE)")
			self._connection.commit()
			last_row = cursor.lastrowid
			cursor.execute("UPDATE Student_users SET CartID = '{}' WHERE Email_Address = '{}'".format(last_row, self._username))
			self._connection.commit()
			self.cartId = last_row
		
		self.book_image = ImageTk.PhotoImage(image)
		self.book_label = Label(self.window, image=self.book_image, height=100, width=100, border=0)
		self.book_label.pack(anchor="center");

		self.title_label = Label(self.window, text="UST Books", font=("Arial", 20, "bold"), background='white')
		self.title_label.pack()

		self.recommendations_label = Label(self.window, text="View recommendations", font=("Arial", 14, "normal"), background='white')
		self.recommendations_label.pack()
		self.recommendations_label.bind("<Button-1>", self.openRec)

		self.search_frame = Frame(self.window, width=200, height=200, background='white', pady=20)
		self.search_frame.pack();

		self.search_frame.columnconfigure(0, weight=1)
		self.search_frame.columnconfigure(1, weight=1)

		self.search = Entry(self.search_frame, background='white')
		self.search_button = Button(self.search_frame, background='white', text='Search', command=self.searchBooks)

		self.search.grid(column=0, row=0)
		self.search_button.grid(column=1, row=0)

		self.frame_table = Frame(self.window, width=400, background='white')
		self.frame_table.pack(fill="both", expand=True)

		self.tree = Treeview(self.frame_table, columns=("Book", "Rating", "Review", "Add"), show="headings")
		self.tree.heading("Book", text="Book")
		self.tree.heading("Rating", text="Rating")
		self.tree.heading("Review", text="Review")
		self.tree.heading("Add", text="Add")

		self.tree.column("Book", width=250)
		self.tree.column("Rating", width=25)
		self.tree.column("Review", width=50)
		self.tree.column("Add", width=25)

		self.tree.bind("<ButtonRelease-1>", self.tree_click)


		self.window.config(background='white')
		self.window.mainloop()

	def searchBooks(self):
		self.tree.delete(*self.tree.get_children())

		search = self.search.get()
		if search != None:
			rows = self._connection.execute("SELECT Books.Title, COALESCE(AVG(Reviews.Rating), 0) AS TotalRating FROM Books LEFT JOIN Reviews ON Books.ISBN = Reviews.ISBN WHERE Books.Title LIKE '%" + search + "%' GROUP BY Books.Title").fetchall()
			print(rows)
			for i, (title, rating) in enumerate(rows):
				if rating == 0:
					rating = "None";
				self.tree.insert("", "end", values=(title, rating, "Review Book", "Add to Cart"))

			self.tree.pack(fill="both", expand=True)
		
	def tree_click(self, event):
		region = self.tree.identify("region", event.x, event.y)

		if region == "cell":
			column = self.tree.identify_column(event.x)
			if column == "#3":  # Check if the clicked column is the "Review" column
				item_id = self.tree.identify_row(event.y)
				item_values = self.tree.item(item_id, "values")
				self.window.destroy()
				StudentReview(self._username, self._password, item_values[0], self._mainwindow, self._connection, self.cartId)
			if column == "#4":
				item_id = self.tree.identify_row(event.y)
				book = self.tree.item(item_id, "values")[0]
				self._connection.execute("UPDATE Carts SET Modified_Date = CURRENT_DATE WHERE CartID = '{}'".format(self.cartId))
				self._connection.commit()

				isbn = self._connection.execute("SELECT ISBN FROM Books WHERE Title = '{}'".format(book)).fetchone()[0]

				self._connection.execute("INSERT INTO CartBooks (CartID, ISBN) Values ('{}','{}')".format(self.cartId, isbn))
				self._connection.commit()
				messagebox.showinfo("UST Books: Cart Operation", "The book was added successfully")

	def ongoingOrders(self):
		self.window.destroy()
		StudentOngoingOrders(self._username, self._password, self.cartId, self._mainwindow, self._connection)

	def openCart(self):
		self.window.destroy();
		StudentCart(self._username, self._password, self.cartId, self._mainwindow, self._connection)

	
	def openRec(self, e):
		self.window.destroy()
		StudentRecommendations(self._username, self._password, self.cartId, self._mainwindow, self._connection)

	def logout(self):
		self.window.destroy()
		self._connection.close()
		self._mainwindow()

class StudentRecommendations:
	def __init__(self, username, password, cartId, mainwindow, conn):
		self.window = Tk()
		self.window.geometry('800x600')
		self.window.title("UST Books")

		self._connection = conn
		self._username = username
		self._password = password

		self._mainwindow = mainwindow;

		self.set_frame = Frame(self.window, width=100, height=50)
		self.set_frame.pack(anchor='ne')

		self.set_frame.grid_columnconfigure(0, weight=1)
		self.set_frame.grid_columnconfigure(1, weight=1)
		self.set_frame.grid_columnconfigure(2, weight=1)

		self.cart_label = Button(self.set_frame, text="Cart", command=self.openCart)
		self.logout_label = Button(self.set_frame, text="Logout", command=self.logout)
		self.orders = Button(self.set_frame, text="Ongoing Orders", command=self.ongoingOrders)
		self.cart_label.grid(column=0, row=0)
		self.logout_label.grid(column=2, row=0)
		self.orders.grid(column=1, row=0)

		self.cartId = cartId

		self.recs = []

		recs = self._connection.execute("SELECT First_Name, Last_Name, Title FROM Student_users s INNER JOIN Recommendations r ON s.StudentID = r.StudentID INNER JOIN Books b ON r.ISBN = b.ISBN").fetchall()
		
		for rec in recs:
			print(rec)
			self.recs.append((rec[0], rec[1], rec[2]))
		
		self.book_image = ImageTk.PhotoImage(image)
		self.book_label = Label(self.window, image=self.book_image, height=100, width=100, border=0)
		self.book_label.pack(anchor="center");

		self.title_label = Label(self.window, text="UST Books", font=("Arial", 20, "bold"), background='white')
		self.title_label.pack()

		self.recommendations_label = Label(self.window, text="View Catalog", font=("Arial", 14, "normal"), background='white')
		self.recommendations_label.pack()
		self.recommendations_label.bind("<Button-1>", self.openSearch)

		self.frame_table = Frame(self.window, width=400, background='white')
		self.frame_table.pack(fill="both", expand=True)

		self.tree = Treeview(self.frame_table, columns=("First Name", "Last Name", "Book", "Add"), show="headings")
		self.tree.heading("First Name", text="First Name")
		self.tree.heading("Last Name", text="Last Name")
		self.tree.heading("Book", text="Book")
		self.tree.heading("Add", text="Add")

		self.tree.column("First Name", width=20)
		self.tree.column("Last Name", width=20)
		self.tree.column("Book", width=270)
		self.tree.column("Add", width=25)

		self.tree.bind("<ButtonRelease-1>", self.tree_click)

		for i, (fn, ln, book) in enumerate(self.recs):
			self.tree.insert("", "end", values=(fn, ln, book, "Add to Cart"))

		self.tree.pack(fill="both", expand=True)


		self.window.config(background='white')
		self.window.mainloop()

	def ongoingOrders(self):
		self.window.destroy()
		StudentOngoingOrders(self._username, self._password, self.cartId, self._mainwindow, self._connection)

	def openCart(self):
		self.window.destroy();
		StudentCart(self._username, self._password, self.cartId, self._mainwindow, self._connection)

	def logout(self):
		self.window.destroy()
		self._connection.close()
		self._mainwindow()

	def openSearch(self, e):
		username = self._username
		password = self._password
		mainwindow = self._mainwindow
		self.window.destroy()
		Student(username, password, mainwindow, self._connection)

	def tree_click(self, event):
		region = self.tree.identify("region", event.x, event.y)

		if region == "cell":
			column = self.tree.identify_column(event.x)
			if column == "#4":
				item_id = self.tree.identify_row(event.y)
				book = self.tree.item(item_id, "values")[2]
				self._connection.execute("UPDATE Carts SET Modified_Date = CURRENT_DATE WHERE CartID = '{}'".format(self.cartId))
				self._connection.commit()

				isbn = self._connection.execute("SELECT ISBN FROM Books WHERE Title = '{}'".format(book)).fetchone()[0]

				self._connection.execute("INSERT INTO CartBooks (CartID, ISBN) Values ('{}','{}')".format(self.cartId, isbn))
				self._connection.commit()
				
				messagebox.showinfo("UST Books: Cart Operation", "The book was added successfully")



class StudentOngoingOrders:
	def __init__(self, username, password, cartId, mainWindow, conn):
		self.window = Tk()
		self.window.geometry('800x600')
		self.window.title("UST Books")

		self._connection = conn
		self._username = username
		self._password = password

		self._mainwindow = mainWindow
		self.cartId = cartId

		self.set_frame = Frame(self.window, width=100, height=50)
		self.set_frame.pack(anchor='ne')

		self.set_frame.grid_columnconfigure(0, weight=1)
		self.set_frame.grid_columnconfigure(1, weight=1)
		self.set_frame.grid_columnconfigure(2, weight=1)

		self.book_label = Button(self.set_frame, text="Books", command=self.openSearch)
		self.cart_label = Button(self.set_frame, text="Cart", command=self.openCart)
		self.logout_label = Button(self.set_frame, text="Logout", command=self.logout)
		self.book_label.grid(column=0, row=0)
		self.cart_label.grid(column=1, row=0)
		self.logout_label.grid(column=2, row=0)


		studentId = self._connection.execute("SELECT StudentID FROM Student_users WHERE Email_Address = '{}'".format(self._username)).fetchone()[0]
		self.studentId = studentId

		self.orders = [];

		orders = self._connection.execute("SELECT OrderID, Created_Date FROM Orders WHERE Fulfilled_Date IS NULL AND Created_Date IS NOT NULL AND StudentID = '{}'".format(self.studentId)).fetchall()

		for order in orders:
			self.orders.append((order[0], order[1]))

		self.book_image = ImageTk.PhotoImage(image)
		self.book_label = Label(self.window, image=self.book_image, height=100, width=100, border=0)
		self.book_label.pack(anchor="center");

		self.title_label = Label(self.window, text="UST Books", font=("Arial", 20, "bold"), background='white')
		self.title_label.pack()

		self.cart_label = Label(self.window, text="Ongoing Orders", font=("Arial", 20, "bold"), background='white')
		self.cart_label.pack()

		self.frame_table = Frame(self.window, width=400, background='white')
		self.frame_table.pack(fill="both", expand=True)

		self.tree = Treeview(self.frame_table, columns=("Order ID", "Ordered Date", "Cancel"), show="headings")
		self.tree.heading("Order ID", text="Order ID")
		self.tree.heading("Ordered Date", text="Ordered Date")
		self.tree.heading("Cancel", text="Cancel")

		self.tree.column("Order ID", width=100)
		self.tree.column("Ordered Date", width=150)
		self.tree.column("Cancel", width=100)

		for i, (orderid, date) in enumerate(self.orders):
			self.tree.insert("", "end", values=(orderid, date, "Cancel"))

		self.tree.bind("<ButtonRelease-1>", self.tree_click)

		self.tree.pack()

		self.window.config(background='white')
		self.window.mainloop()

	def openSearch(self):
		username = self._username
		password = self._password
		mainwindow = self._mainwindow
		self.window.destroy()
		Student(username, password, mainwindow, self._connection)

	def tree_click(self, event):
		region = self.tree.identify("region", event.x, event.y)

		if region == "cell":
			column = self.tree.identify_column(event.x)
			if column == "#3":  # Check if the clicked column is the "Review" column
				item_id = self.tree.identify_row(event.y)
				item_values = self.tree.item(item_id, "values")
				self.tree.delete(item_id)

				self._connection.execute("DELETE FROM Orders WHERE OrderId = '{}'".format(item_values[0]))
				self._connection.commit()

	def openCart(self):
		self.window.destroy();
		StudentCart(self._username, self._password, self.cartId, self._mainwindow, self._connection)

	def logout(self):
		self.window.destroy()
		self._connection.close()
		self._mainwindow()



class StudentReview:
	def __init__(self, username, password, book, mainwindow, conn, cartId):
		self.window = Tk()
		self.window.geometry('800x600')
		self.window.title("UST Books")

		self._username = username
		self._password = password

		self._book = book

		self._mainwindow = mainwindow
		self.conn = conn
		self.cartId = cartId

		self.set_frame = Frame(self.window, width=100, height=50)
		self.set_frame.pack(anchor='ne')

		self.set_frame.grid_columnconfigure(0, weight=1)
		self.set_frame.grid_columnconfigure(1, weight=1)

		self.cart_label = Button(self.set_frame, text="Books", command=self.openSearch)
		self.logout_label = Button(self.set_frame, text="Logout", command=self.logout)
		self.cart_label.grid(column=0, row=0)
		self.logout_label.grid(column=1, row=0)


		self.book_image = ImageTk.PhotoImage(image)
		self.book_label = Label(self.window, image=self.book_image, height=100, width=100, border=0)
		self.book_label.pack(anchor="center");

		self.title_label = Label(self.window, text="UST Books", font=("Arial", 20, "bold"), background='white')
		self.title_label.pack()

		self.book_title = Label(self.window, text=book, font=("Arial", 16, "bold"), background="white", wraplength=400)
		self.book_title.pack()

		self.rating_label = Label(self.window, text="Rating", background='white')
		self.rating_label.pack()
		
		self.rating = Combobox(self.window, values=["1", "2", "3", "4", "5"], font=("Arial", 12, "bold"), background="white")
		self.rating.pack()
		
		self.reco_value = IntVar()

		self.reco = Checkbutton(self.window, text="Would you recommend this book to other students?", variable=self.reco_value, font=("Arial", 10, "normal"), background="white")
		self.reco.pack()


		self.rating_desc_label = Label(self.window, text="Review Description", background='white')
		self.rating_desc_label.pack()

		self.rating_desc = Text(self.window, background='white', font=("Arial", 12, "normal"), height=8, width=30)
		self.rating_desc.pack()

		self.submit = Button(self.window, text="Submit review", command=self.submit_review)
		self.submit.pack(pady=10)

		self.window.config(background='white')
		self.window.mainloop()
	
	def logout(self):
		self.window.destroy()
		self.conn.close()
		self._mainwindow()
	def openSearch(self):
		username = self._username
		password = self._password
		mainwindow = self._mainwindow
		self.window.destroy()
		Student(username, password, mainwindow, self.conn)

	def submit_review(self):
		
		book = self.book_title.cget('text')
		rating = self.rating.get()
		desc = self.rating_desc.get('1.0', END)
		rec = self.reco_value.get()
		print(rec)

		isbn = self.conn.execute("SELECT ISBN FROM Books WHERE Title = '{}'".format(book)).fetchone()[0]
		studentId = self.conn.execute("SELECT StudentID FROM Student_users WHERE Email_Address = '{}'".format(self._username)).fetchone()[0]

		self.conn.execute("INSERT INTO Reviews (StudentID, ISBN, Rating, Review_Description) Values ('{}','{}','{}','{}')".format(studentId, isbn, rating, desc))
		self.conn.commit()

		if rec == 1:
			self.conn.execute("INSERT INTO Recommendations (StudentID, ISBN) Values ('{}', '{}')".format(studentId, isbn))
			self.conn.commit()

		self.openSearch()



class StudentCart:
	def __init__(self, username, password, cart, mainwindow, connection):
		self.window = Tk()
		self.window.geometry('800x600')
		self.window.title("UST Books")

		self._username = username
		self._password = password

		self._mainwindow = mainwindow
		self.connection = connection;
		
		self.cartId = cart;

		self.cart = []

		#Setup Cart
		books = self.connection.execute("SELECT Title FROM Books JOIN CartBooks ON Books.ISBN = CartBooks.ISBN WHERE CartBooks.CartID = '{}'".format(self.cartId)).fetchall()
		
		for book in books:
			self.cart.append((book[0], 1))

		self.set_frame = Frame(self.window, width=100, height=50)
		self.set_frame.pack(anchor='ne')

		self.set_frame.grid_columnconfigure(0, weight=1)
		self.set_frame.grid_columnconfigure(1, weight=1)
		self.set_frame.grid_columnconfigure(2, weight=1)

		self.cart_label = Button(self.set_frame, text="Books", command=self.openSearch)
		self.logout_label = Button(self.set_frame, text="Logout", command=self.logout)
		self.orders = Button(self.set_frame, text="Ongoing Orders", command=self.ongoingOrders)
		self.cart_label.grid(column=0, row=0)
		self.logout_label.grid(column=2, row=0)
		self.orders.grid(column=1, row=0)


		self.book_image = ImageTk.PhotoImage(image)
		self.book_label = Label(self.window, image=self.book_image, height=100, width=100, border=0)
		self.book_label.pack(anchor="center");

		self.title_label = Label(self.window, text="UST Books", font=("Arial", 20, "bold"), background='white')
		self.title_label.pack()

		self.cart_label = Label(self.window, text="Cart", font=("Arial", 20, "bold"), background='white')
		self.cart_label.pack()


		self.frame_table = Frame(self.window)
		self.frame_table.pack()

		self.tree = Treeview(self.frame_table, columns=("Book", "Quantity", "Remove"), show="headings")
		self.tree.heading("Book", text="Book")
		self.tree.heading("Quantity", text="Quantity")
		self.tree.heading("Remove", text="Remove")

		self.tree.column("Book", width=200)
		self.tree.column("Quantity", width=50)
		self.tree.column("Remove", width=50)

		self.tree.bind("<ButtonRelease-1>", self.tree_click)

		for i, (title, quantity) in enumerate(self.cart):
			self.tree.insert("", "end", values=(title, quantity, "Remove"))

		self.tree.pack(fill="both", expand=True)

		checkout = Button(self.window, text="Checkout", command=self.checkout)
		checkout.pack()

		self.window.config(background='white')
		self.window.mainloop()

	def ongoingOrders(self):
		self.window.destroy()
		StudentOngoingOrders(self._username, self._password, self.cartId, self._mainwindow, self.connection)

	def tree_click(self, event):
		region = self.tree.identify("region", event.x, event.y)

		if region == "cell":
			column = self.tree.identify_column(event.x)
			if column == "#3":
				item_id = self.tree.identify_row(event.y)
				book = self.tree.item(item_id, "values")[0]

				self.connection.execute("UPDATE Carts SET Modified_Date = CURRENT_DATE WHERE CartID = '{}'".format(self.cartId))
				self.connection.commit()

				isbn = self.connection.execute("SELECT ISBN FROM Books WHERE Title = '{}'".format(book)).fetchone()[0]
				rowid = self.connection.execute("SELECT rowID FROM CartBooks Where CartId = '{}' AND ISBN = '{}'".format(self.cartId, isbn)).fetchone()[0]

				self.connection.execute("DELETE FROM CartBooks WHERE RowID = '{}'".format(rowid))
				self.connection.commit()

				self.tree.delete(item_id)

	def logout(self):
		self.window.destroy()
		self.connection.close()
		self._mainwindow()

	def openSearch(self):
		username = self._username
		password = self._password
		self.window.destroy()
		Student(username, password, self._mainwindow, self.connection)

	def checkout(self):
		if len(self.cart) == 0:
			messagebox.showerror("UST Books: Checkout Error", "You have nothing in your cart you silly goose")
		else:
			username = self._username
			password = self._password
			self.window.destroy()
			StudentCheckout(username, password, self.cartId, self._mainwindow, self.connection)


class StudentCheckout:
	def __init__(self, username, password, cart, mainwindow, connection):
		self.window = Tk()
		self.window.geometry('800x600')
		self.window.title("UST Books")

		self._mainwindow = mainwindow
		self.connection = connection
		self.cartId = cart

		books = self.connection.execute("SELECT Title FROM Books JOIN CartBooks ON Books.ISBN = CartBooks.ISBN WHERE CartBooks.CartID = '{}'".format(self.cartId)).fetchall()
		
		self.cart = []
		for book in books:
			self.cart.append((book[0], 1))

		self._username = username
		self._password = password
		self._address = None;
		self._card = None;
		self._csv = None;

		self.set_frame = Frame(self.window, width=100, height=50)
		self.set_frame.pack(anchor='ne')

		self.set_frame.grid_columnconfigure(0, weight=1)
		self.set_frame.grid_columnconfigure(1, weight=1)

		self.cart_label = Button(self.set_frame, text="Cart", command=self.openCart)
		self.logout_label = Button(self.set_frame, text="Logout", command=self.logout)
		self.cart_label.grid(column=0, row=0)
		self.logout_label.grid(column=1, row=0)


		self.book_image = ImageTk.PhotoImage(image)
		self.book_label = Label(self.window, image=self.book_image, height=100, width=100, border=0)
		self.book_label.pack(anchor="center");

		self.title_label = Label(self.window, text="UST Books", font=("Arial", 20, "bold"), background='white')
		self.title_label.pack()

		self.cart_label = Label(self.window, text="Checkout", font=("Arial", 20, "bold"), background='white')
		self.cart_label.pack()


		self.frame_table = Frame(self.window)
		self.frame_table.pack()

		column_headers = ["Book", "Quantity"]

		for i, header in enumerate(column_headers):
				label = Label(self.frame_table, text=header)
				label.grid(row=0, column=i)
		for i, (book) in enumerate(self.cart):
				label_book = Label(self.frame_table, text=book[0])
				label_book.grid(row=i+1, column=0)

				label_quantity = Label(self.frame_table, text=1)
				label_quantity.grid(row=i+1, column=1)
		

		self.address = Entry(self.window, background='white')
		self.address.bind("<FocusIn>", self.on_entry_click)
		self.address.bind("<FocusOut>", self.on_entry_leave)
		self.address.config(fg="grey")  # Change text color back to grey
		self.address.pack()

		self.card = Entry(self.window, background='white')
		self.card.bind("<FocusIn>", self.on_entry_click)
		self.card.bind("<FocusOut>", self.on_entry_leave)
		self.card.config(fg="grey")  # Change text color back to grey
		self.card.pack()

		# Prefill daata
		if self._address:
			self.address.insert(0, self._address)
		else:
			self.address.insert(0, "Address")

		if self._card:
			self.card.insert(0, self._card)
		else:
			self.card.insert(0, "Card")

		checkout = Button(self.window, text="Submit order", command=self.submitOrder)
		checkout.pack()

		self.window.config(background='white')
		self.window.mainloop()

	def on_entry_click(self, event):
		if event.widget.get() == "Address":
				self.address.delete(0, "end")
				self.address.config(fg="black")  # Change text color when the user starts typing
		if event.widget.get() == "Card":
				self.card.delete(0, "end")
				self.card.config(fg="black")  # Change text color when the user starts typing

	def on_entry_leave(self, event):
		if event.widget.get() == "" and event.widget == self.address:
				event.widget.insert(0, "Address")
				self.address.config(fg="grey")  # Change text color back to grey
		if event.widget.get() == "" and event.widget == self.card:
				self.card.insert(0, "Card")
				self.card.config(fg="grey")  # Change text color back to grey

	def submitOrder(self):
		studentId = self.connection.execute("SELECT StudentID FROM Student_users WHERE Email_Address = '{}'".format(self._username)).fetchone()[0]
		card = self.card.get()

		cursor = self.connection.execute("INSERT INTO Orders (StudentID, CartID, Created_Date, Card_Number) Values ('{}', '{}', CURRENT_DATE, '{}')".format(studentId, self.cartId, card))
		self.connection.commit()

		lastRow = cursor.lastrowid

		for book, quantity in self.cart:
			isbn = self.connection.execute("SELECT ISBN FROM Books WHERE Title = '{}'".format(book)).fetchone()[0]

			self.connection.execute("INSERT INTO OrderBooks (ISBN, OrderID, Quantity) Values ('{}', '{}', '{}')".format(isbn, lastRow, quantity))
			self.connection.commit()
			self.connection.execute("DELETE FROM CartBooks WHERE ISBN = '{}'".format(isbn))
			self.connection.commit()
		
		self.connection.execute("UPDATE Carts SET Modified_Date = CURRENT_DATE WHERE CartId = '{}'".format(self.cartId))
		self.openCart()

	def openCart(self):
		self.window.destroy();
		StudentCart(self._username, self._password, self.cartId, self._mainwindow, self.connection)

	def logout(self):
		self.window.destroy()
		self.connection.close()
		self._mainwindow()
