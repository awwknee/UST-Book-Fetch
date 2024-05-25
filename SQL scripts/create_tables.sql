PRAGMA foreign_keys=ON;

create table if not exists
  Carts (
    CartID INTEGER PRIMARY KEY AUTOINCREMENT,
    Created_Date TEXT,
    Modified_Date TEXT
  );

create table if not exists
  Universities (
    UniversityID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(255),
    Address VARCHAR(255),
    Rep_First_Name VARCHAR(255),
    Rep_Last_Name VARCHAR(255),
    Rep_Email_Address VARCHAR(255),
    Rep_Phone_Number VARCHAR(10)
  );

create table if not exists
  Student_users (
    StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
    Password VARCHAR(255),
    UniversityID INT,
    CartID INT,
    First_Name VARCHAR(255),
    Last_Name VARCHAR(255),
    Email_Address VARCHAR(255),
    Address VARCHAR(255),
    Phone_Number VARCHAR(10),
    Birth_Date TEXT,
    Major VARCHAR(255),
    Status VARCHAR(9) check (Status in ('UnderGrad', 'Grad')),
    year SMALLINT,
    FOREIGN KEY (UniversityID) references Universities (UniversityID) ON DELETE CASCADE,
    FOREIGN KEY (CartID) references Carts (CartID) ON DELETE CASCADE
);

create table if not exists
  Books (
    ISBN INTEGER PRIMARY KEY AUTOINCREMENT,
    Title VARCHAR(255),
    type VARCHAR(255),
    Price decimal(7, 2),
    Author VARCHAR(255),
    Publisher VARCHAR(255),
    Publish_Date Date,
    language VARCHAR(255)
);

create table if not exists
  CartBooks (
	ISBN INT,
    CartID INT,
    FOREIGN KEY (ISBN) references books (ISBN) ON DELETE CASCADE,
    FOREIGN KEY (CartID) references Carts (CartID) ON DELETE CASCADE
  );

create table if not exists
  Reviews (
    ReviewID INTEGER PRIMARY KEY AUTOINCREMENT,
    StudentID INT,
    ISBN INT,
    Rating INT,
    Review_Description VARCHAR(255),
    FOREIGN KEY (StudentID) references student_users (StudentID) ON DELETE CASCADE,
    FOREIGN KEY (ISBN) references Books (ISBN) ON DELETE CASCADE
);

create table if not exists
  Recommendations (
    StudentID INT,
    ISBN INT,
    FOREIGN KEY (StudentID) references Student_users (StudentID) ON DELETE CASCADE,
    FOREIGN KEY (ISBN) references Books (ISBN) ON DELETE CASCADE
);

create table if not exists
  Administrators (
    AEmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
    Password VARCHAR(255),
    First_Name VARCHAR(255),
    Last_Name VARCHAR(255),
    Gender VARCHAR(6) check (Gender in ('Male', 'Female', 'Other')),
    Salary INT,
    SSN VARCHAR(9),
    Email_Address VARCHAR(255) unique,
    Address VARCHAR(255),
    Phone_Number VARCHAR(10)
  );

create table if not exists
  Customer_support_users (
    CSEmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
    Password VARCHAR(255),
    First_Name VARCHAR(255),
    Last_Name VARCHAR(255),
    Gender VARCHAR(6) check (Gender in ('Male', 'Female', 'Other')),
    Salary INT,
    SSN VARCHAR(9),
    Email_Address VARCHAR(255) unique,
    Address VARCHAR(255),
    Phone_Number VARCHAR(10)
  );


create table if not exists
  Trouble_Tickets (
    TicketID INTEGER PRIMARY KEY AUTOINCREMENT,
    Ticket VARCHAR(255),
    Category VARCHAR(255) check (Category in ('userprofile', 'products', 'orders', 'cart', 'other')),
    Date_Logged Date,
    StudentID INT,
    AEmployeeID INT,
    CSEmployeeID INT,
    Title VARCHAR(255),
    Date_Completed TEXT,
    Problem_Description VARCHAR(255),
    Solution_Description VARCHAR(255),
    Status VARCHAR(20) check (Status in ('new', 'assigned', 'in-process', 'completed')),
    FOREIGN KEY (StudentID) references Student_users (StudentID) ON DELETE CASCADE,
    FOREIGN KEY (AEmployeeID) references Administrators (AEmployeeID) ON DELETE SET NULL,
    FOREIGN KEY (CSEmployeeID) references Customer_support_users (CSEmployeeID) ON DELETE SET NULL
  );

create table if not exists
  Departments (
    DepartmentID INTEGER PRIMARY KEY AUTOINCREMENT,
    UniversityID INT,
    name VARCHAR(255),
    FOREIGN KEY (UniversityID) references Universities (UniversityID) ON DELETE CASCADE
);

create table if not exists
  Instructors (
    InstructorID INT,
    DepartmentID INT,
    UniversityID INT,
    First_Name VARCHAR(255),
    Last_Name VARCHAR(255),
    FOREIGN KEY (DepartmentID) references Departments (DepartmentID) ON DELETE CASCADE,
    FOREIGN KEY (UniversityID) references Universities (UniversityID) ON DELETE CASCADE
);

create table if not exists
  Courses (
    CourseID INTEGER PRIMARY KEY AUTOINCREMENT,
    UniversityID INT,
    DepartmentID INT,
    name VARCHAR(255),
    year INT,
    Semester INT,
    FOREIGN KEY (UniversityID) references Universities (UniversityID) ON DELETE CASCADE,
    FOREIGN KEY (DepartmentID) references Departments (DepartmentID) ON DELETE CASCADE
  );
  
create table if not exists
  CourseReadings (
	CourseID INT,
    ISBN INT,
    FOREIGN KEY (CourseID) references Courses (CourseID) ON DELETE CASCADE,
    FOREIGN KEY (ISBN) references Books (ISBN) ON DELETE CASCADE
);

create table if not exists
  InstructorCourses (
	CourseID INT,
    InstructorID INT,
    FOREIGN KEY (CourseID) references Courses (CourseID) ON DELETE CASCADE,
    FOREIGN KEY (InstructorID) references Instructors (InstructorID) ON DELETE CASCADE
);

create table if not exists
  Orders (
    OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
    StudentID INT,
    CartID INT,
    Created_Date Date,
    Fulfilled_Date Date,
    Card_Number VARCHAR(16),
    Card_Exp_Date TEXT,
    Card_Name VARCHAR(255),
    Card_Type VARCHAR(255),
    Status VARCHAR(20) check (Status in ('shipped', 'shipping', 'cancelled', 'new')),
    Ship_Type VARCHAR(20) check (Ship_type in ('1-day', 'standard', '2-day')),
    FOREIGN KEY (StudentID) references Student_users (StudentID) ON DELETE CASCADE,
    FOREIGN KEY (CartID) references Carts (CartID) ON DELETE CASCADE
  );
  
  create table if not exists
  OrderBooks (
	ISBN INT,
    OrderID INT,
    Type VARCHAR(8) check (Type in ('rent', 'purchase')),
    Quantity INT,
    FOREIGN KEY (ISBN) references books (ISBN) ON DELETE CASCADE,
    FOREIGN KEY (OrderID) references Orders (OrderID) ON DELETE CASCADE
  );

create table if not exists
  Super_administrators (
    SAEmployeeID INT,
    Password VARCHAR(255),
    First_Name VARCHAR(255),
    Last_Name VARCHAR(255),
    Gender VARCHAR(6) check (Gender in ('Male', 'Female', 'Other')),
    Salary INT,
    SSN VARCHAR(9),
    Email_Address VARCHAR(255) unique,
    Address VARCHAR(255),
    Phone_Number VARCHAR(10)
  );

create table if not exists
  Categories (
    CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(255)
  );

create table if not exists
  Subcategories (
    SubcategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(255)
  );

create table if not exists
  BookCategories (
    ISBN INT,
    CategoryID INT,
    FOREIGN KEY (ISBN) references books (ISBN) ON DELETE CASCADE,
    FOREIGN KEY (CategoryID) references categories (CategoryID) ON DELETE CASCADE 
  );

create table if not exists
  BookSubcategories (
    ISBN INT,
    SubcategoryID INT,
    FOREIGN KEY (ISBN) references books (ISBN) ON DELETE CASCADE,
    FOREIGN KEY (SubcategoryID) references subcategories (SubcategoryID) ON DELETE CASCADE
  );



    
    
    


