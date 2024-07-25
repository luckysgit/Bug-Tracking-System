import mysql.connector

class GetBTSDB:
    def __init__(self):
        self.db = mysql.connector.connect(host="localhost", database="bts", user="root", password="")

class LoginSignup(GetBTSDB):
    def __init__(self):
        super().__init__()
        print("")
        self.custLoginId = ""
        self.custPassword = ""
        self.custName = ""
        self.custAge = 0
        self.custPhone = ""
        self.custEmail = ""

    def identity(self):
        user = input("Welcome\n* If you already have an account: For login = press L\n- For creating a new account: Type signup = press S\n")

        if user == "L":
            self.login()
        elif user == "S":
            self.signup()
        else:
            print("Invalid choice.")

    def login(self):
        print("Welcome to bts")

        who = input("Who are you: customer(C/c) / employee(E/e) ")
        LoginId = input("Enter LoginId: ")
        password = input("Enter Password: ")

        mycursor = self.db.cursor()

        if who == "c":
            sql = "SELECT * FROM customer WHERE custLoginId = %s"
        elif who == "e":
            sql = "SELECT * FROM employee WHERE empLoginId = %s"
        else:
            print("Invalid user type.")
            return

        value = (LoginId,)

        mycursor.execute(sql, value)
        row = mycursor.fetchone()

        if row is not None:
            dbPass = row[1]
            if password == dbPass:
                print("Login authentication success")
                if who == "c":
                    print("Welcome", LoginId)
                    self.customerActions(LoginId)
                elif who == "e":
                    print("Welcome", row[2])
                else:
                    print("Invalid user type.")
            else:
                print("Login authentication failed")
        else:
            print("Invalid ID. Please retry...")

        mycursor.close()

    def signup(self):
        print("Welcome to signup page")

        user = input("Who are you: customer(C/c) / employee(E/e) ")

        if user == "c":
            custLoginId = input("Enter login-id: ")
            custPassword = input("Enter password: ")
            custName = input("Enter name: ")
            custAge = int(input("Enter age: "))
            custPhone = input("Enter phone no: ")
            custEmail = input("Enter email: ")

            sql = "INSERT INTO customer(custLoginId, custPassword, custName, custAge, custPhone, custEmail) " \
                  "VALUES(%s, %s, %s, %s, %s, %s)"
            value = (custLoginId, custPassword, custName, custAge, custPhone, custEmail)

            mycursor = self.db.cursor()
            mycursor.execute(sql, value)
            self.db.commit()
            mycursor.close()

            print("Signup successful for", custLoginId)
        elif user == "e":
            empLoginId = input("Enter login-id: ")
            empPassword = input("Enter password: ")
            empType = input("Enter type (ADMIN / EXPERT): ")

            if empType.lower() == "admin" or empType.lower() == "expert":
                empName = input("Enter name: ")
                empPhone = input("Enter phone no: ")
                empEmail = input("Enter email: ")

                sql = "INSERT INTO employee(empLoginId, empPassword, empType, empName, empPhone, empEmail) " \
                      "VALUES(%s, %s, %s, %s, %s, %s)"
                value = (empLoginId, empPassword, empType, empName, empPhone, empEmail)

                mycursor = self.db.cursor()
                mycursor.execute(sql, value)
                self.db.commit()
                mycursor.close()

                print("Signup successful for", empLoginId)
            else:
                print("Type only Admin / Expert")
        else:
            print("Invalid user type.")

        self.db.close()

    def customerActions(self, custLoginId):
        while True:
            action = input("Choose an action:\n1. Update Profile\n2. Logout\n")

            if action == "1":
                self.updateProfile(custLoginId)
            elif action == "2":
                print("Logged out successfully")
                break
            else:
                print("Invalid action")

    def updateProfile(self, custLoginId):
        mycursor = self.db.cursor()
        sql = "SELECT * FROM customer WHERE custLoginId = %s"
        value = (custLoginId,)
        mycursor.execute(sql, value)
        row = mycursor.fetchone()

        if row is not None:
            print("Existing Profile:")
            print("Customer ID:", row[0])
            print("Name:", row[2])
            print("Age:", row[3])
            print("Phone:", row[4])
            print("Email:", row[5])

            newCustName = input("Enter new name: ")
            newCustAge = int(input("Enter new age: "))
            newCustPhone = input("Enter new phone: ")
            newCustEmail = input("Enter new email: ")

            update_sql = "UPDATE customer SET custName = %s, custAge = %s, custPhone = %s, custEmail = %s WHERE custLoginId = %s"
            update_value = (newCustName, newCustAge, newCustPhone, newCustEmail, custLoginId)
            mycursor.execute(update_sql, update_value)
            self.db.commit()
            print("Profile updated successfully")
        else:
            print("Customer ID not found.")

        mycursor.close()

# Create an instance of the LoginSignup class
module_a = LoginSignup()

# Call the identity method
module_a.identity()

