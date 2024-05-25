import sqlite3
import sys

connection = sqlite3.connect('./ustbooks.db');
connection.execute("PRAGMA foreign_keys = ON")
connection.commit()

queries = [
  "SELECT * FROM Student_users s JOIN Universities u ON s.UniversityID = u.UniversityID WHERE u.name = 'UST'",
  "SELECT * FROM Student_users WHERE Status = 'Grad'",
  "SELECT s.* FROM Student_users s JOIN Orders o ON s.StudentID = o.StudentID JOIN OrderBooks ob ON o.OrderID = ob.OrderID WHERE s.Major = 'Computer Science' AND ob.Type = 'purchase' GROUP BY s.StudentID HAVING AVG(ob.Quantity) > 2",
  "SELECT b.Title, b.ISBN FROM Books b JOIN OrderBooks ob ON b.ISBN = ob.ISBN GROUP BY b.ISBN ORDER BY COUNT(ob.ISBN) DESC",
  "SELECT c.Name AS Category, sc.Name AS Subcategory, b.Title, b.ISBN FROM Books b LEFT JOIN BookCategories bc ON b.ISBN = bc.ISBN LEFT JOIN Categories c ON bc.CategoryID = c.CategoryID LEFT JOIN BookSubcategories bsc ON b.ISBN = bsc.ISBN LEFT JOIN Subcategories sc ON bsc.SubcategoryID = sc.SubcategoryID",
  "SELECT co.name AS CourseName, b.Title FROM Courses co JOIN CourseReadings cr ON co.CourseID = cr.CourseID JOIN Books b ON cr.ISBN = b.ISBN LEFT JOIN BookCategories bc ON b.ISBN = bc.ISBN LEFT JOIN Categories c ON bc.CategoryID = c.CategoryID WHERE c.Name <> 'Computer Science' OR c.Name IS NULL",
  "SELECT b.Title, b.ISBN FROM Books b JOIN OrderBooks ob ON b.ISBN = ob.ISBN JOIN Orders o ON ob.OrderID = o.OrderID JOIN Student_users s ON o.StudentID = s.StudentID LEFT JOIN CourseReadings cr ON b.ISBN = cr.ISBN WHERE cr.ISBN IS NULL GROUP BY b.ISBN, b.Title HAVING ((SELECT COUNT(DISTINCT cbc.CategoryID) FROM BookCategories cbc WHERE cbc.ISBN = b.ISBN AND cbc.CategoryID IN (SELECT cbc2.CategoryID FROM CourseReadings cr2 JOIN BookCategories cbc2 ON cr2.ISBN = cbc2.ISBN)) + (SELECT COUNT(DISTINCT cbsc.SubcategoryID) FROM BookSubcategories cbsc WHERE cbsc.ISBN = b.ISBN AND cbsc.SubcategoryID IN (SELECT cbsc2.SubcategoryID FROM CourseReadings cr2 JOIN BookSubcategories cbsc2 ON cr2.ISBN = cbsc2.ISBN))) >= 2",
  "SELECT b.Title, b.ISBN, COUNT(DISTINCT cr.CourseID) AS CourseCount FROM Books b LEFT JOIN CourseReadings cr ON b.ISBN = cr.ISBN GROUP BY b.ISBN",
  "SELECT DISTINCT b.Title FROM Books b WHERE b.Title LIKE '%Linear Algebra%'",
  "SELECT b.Title FROM Books b JOIN Reviews r ON b.ISBN = r.ISBN GROUP BY b.Title HAVING AVG(r.Rating) > 3",
  "SELECT b.Title, COUNT(ob.OrderID) AS PurchaseCount, COALESCE(AVG(r.Rating), 0) AS OverallRating FROM Books b LEFT JOIN OrderBooks ob ON b.ISBN = ob.ISBN LEFT JOIN Reviews r ON b.ISBN = r.ISBN GROUP BY b.Title ORDER BY OverallRating DESC, PurchaseCount DESC",
  "SELECT c.Name AS Category, AVG(ob.Quantity) AS AvgBooksPurchased FROM Categories c JOIN BookCategories bc ON c.CategoryID = bc.CategoryID JOIN OrderBooks ob ON bc.ISBN = ob.ISBN WHERE ob.Type = 'purchase' GROUP BY c.Name",
  "SELECT u.Name AS UniversityName, d.name AS DepartmentName, co.name AS CourseName, COUNT(ic.InstructorID) AS InstructorCount FROM Universities u JOIN Departments d ON u.UniversityID = d.UniversityID JOIN Courses co ON d.DepartmentID = co.DepartmentID LEFT JOIN InstructorCourses ic ON co.CourseID = ic.CourseID GROUP BY u.Name, d.name, co.name",
  "SELECT u.Name AS UniversityName, COUNT(DISTINCT b.ISBN) AS BookCount, SUM(b.Price) AS TotalBookCost FROM Universities u JOIN Student_users su ON u.UniversityID = su.UniversityID JOIN Orders o ON su.StudentID = o.StudentID JOIN OrderBooks ob ON o.OrderID = ob.OrderID JOIN Books b ON ob.ISBN = b.ISBN GROUP BY u.Name",
  "SELECT cs.First_Name, cs.Last_Name, cs.CSEmployeeID, COUNT(t.TicketID) AS TicketCount FROM Customer_support_users cs LEFT JOIN Trouble_Tickets t ON cs.CSEmployeeID = t.CSEmployeeID GROUP BY cs.CSEmployeeID",
  "SELECT a.First_Name, a.Last_Name, a.Salary FROM Administrators a ORDER BY a.Salary DESC",
  "SELECT A.First_Name, A.Last_Name, COUNT(T.TicketID) AS Total_Tickets_Closed FROM Administrators A LEFT JOIN Trouble_Tickets T ON A.AEmployeeID = T.AEmployeeID WHERE T.Status = 'completed' GROUP BY A.AEmployeeID",
  "SELECT T.Status, COUNT(CASE WHEN T.StudentID IS NOT NULL THEN T.TicketID END) AS Total_Student_Created, COUNT(CASE WHEN T.CSEmployeeID IS NOT NULL THEN T.TicketID END) AS Total_Customer_Support_Created FROM Trouble_Tickets T GROUP BY T.Status",
  "SELECT AVG(julianday(Date_Completed) - julianday(Date_Logged)) AS Avg_Time_To_Close FROM Trouble_Tickets WHERE Status = 'completed'",
  "SELECT T.TicketID, T.Title, T.Status, T.Date_Logged, T.Date_Completed, T.Problem_Description, T.Solution_Description FROM Trouble_Tickets T WHERE T.Status = 'completed' ORDER BY T.TicketID",
  "SELECT S.First_Name, S.Last_Name, B.Title AS Recommended_Book FROM Student_users S INNER JOIN Recommendations R ON S.StudentID = R.StudentID INNER JOIN Books B ON R.ISBN = B.ISBN",
  "SELECT B.Title AS Book_Title, COUNT(DISTINCT O.StudentID) AS Count_of_Students FROM Books B LEFT JOIN BookCategories BC ON B.ISBN = BC.ISBN LEFT JOIN OrderBooks OB ON B.ISBN = OB.ISBN LEFT JOIN Orders O ON OB.OrderID = O.OrderID WHERE BC.CategoryID IN (SELECT CategoryID FROM BookCategories WHERE ISBN = B.ISBN) AND O.Status = 'shipped' AND OB.OrderID IS NULL GROUP BY B.ISBN",
  "SELECT B.Title AS Book_Title, AVG(R.Rating) AS Overall_Rating, COUNT(DISTINCT R.StudentID) AS Number_of_Students_Rated FROM Books B LEFT JOIN Reviews R ON B.ISBN = R.ISBN GROUP BY B.ISBN ORDER BY Overall_Rating DESC, Number_of_Students_Rated DESC",
  "SELECT B.Title AS Book_Title, R.Rating, S.First_Name, S.Last_Name, U.Name AS University_Name FROM Books B JOIN Reviews R ON B.ISBN = R.ISBN JOIN Student_users S ON R.StudentID = S.StudentID JOIN Universities U ON S.UniversityID = U.UniversityID WHERE R.Rating = 5"
]

if len(sys.argv) > 1:
  queryNumber = int(sys.argv[1:][0])
  if queryNumber-1 < len(queries) and queryNumber -1 >= 0:
    try:
      print("Query '{}'".format(queryNumber))
      rows = connection.executequeries[queryNumber-1].fetchall()
      print(rows)
    except:
      print("Error with Query '{}'".format(queryNumber))
  else:
    print("That query is not a valid number. Choose between 1 to {}".format(len(queries)))
