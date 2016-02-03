from tkinter import *
import pymysql
from tkinter import messagebox
from Guest import Guest
from Operator import Operator
from Inspector import Inspector

class RestaurantInspectionApp:
    def __init__(self):
        #Connect to the database
        self.db = self.connect()
        self.cursor = self.db.cursor()
        # Login Window
        self.loginWindow = Tk()
        self.loginWindow.title("Georgia  Restaurant Health Inspections")
        self.buildLoginPage(self.loginWindow)

        self.loginWindow.mainloop()

    def buildLoginPage(self, loginWindow):
        # Buttons
        guestButton = Button(loginWindow, text="Guest Login", command=self.guestButtonClicked)
        guestButton.grid(row=2, column=1, sticky=W)

        operatorButton = Button(loginWindow, text="Restaurant Operator Login", command=self.operatorButtonClicked)
        operatorButton.grid(row=3, column=1, sticky=W)

        inspectorButton = Button(loginWindow, text="Health Inspector Login", command=self.inspectorButtonClicked)
        inspectorButton.grid(row=3, column=3, sticky=W)

        # The "/" between Restaurant Operator and Health Inspector
        separateLabel = Label(loginWindow, text="/")
        separateLabel.grid(row=3, column=2, sticky=W)

        # Username Label
        usernameLabel = Label(loginWindow, text="User Name")
        usernameLabel.grid(row=4, column=2, sticky=W)
        # Username Entry
        self.username = StringVar()
        usernameEntry = Entry(loginWindow, textvariable=self.username, width=30)
        usernameEntry.grid(row=4, column=3, sticky=W + E)

        # Password Label
        passwordLabel = Label(loginWindow, text="Password")
        passwordLabel.grid(row=5, column=2, sticky=W)
        # Password Entry
        self.password = StringVar()
        passwordEntry = Entry(loginWindow, textvariable=self.password, show = '*', width=30)
        passwordEntry.grid(row=5, column=3, sticky=W + E)

    # Switch from the login window to the guest menu window
    def guestButtonClicked(self):
        self.loginWindow.withdraw()
        guest = Guest()

    def operatorButtonClicked(self):
        username = self.username.get()
        password = self.password.get()
        if not username:
            messagebox.showwarning("Username input is empty", "Please enter username.")
            return False
        if not password:
            messagebox.showwarning("Password input is empty", "Please enter password")
            return False
        isAnOperatorUsername = self.cursor.execute("SELECT * FROM operatorowner WHERE username = %s", username)
        if not isAnOperatorUsername:
            messagebox.showwarning("Username is not an operator\'s username",
                                   "The username you entered is not an operator\'s username.")
            return False
        usernameAndPasswordMatch = self.cursor.execute(
            "SELECT * FROM registereduser WHERE (username = %s AND password = %s)", (username, password))
        if not usernameAndPasswordMatch:
            messagebox.showwarning("Username and password don\'t match", "Sorry, the username and password you entered"
                                                                         + " do not match.")
            return False
        self.loginWindow.withdraw()
        operator = Operator(username)
        return True

    def inspectorButtonClicked(self):
        username = self.username.get()
        password = self.password.get()
        if not username:
            messagebox.showwarning("Username input is empty", "Please enter username.")
            return False
        if not password:
            messagebox.showwarning("Password input is empty", "Please enter password")
            return False
        isAnInspectorUsername = self.cursor.execute("SELECT * FROM inspector WHERE username = %s", username)
        if not isAnInspectorUsername:
            messagebox.showwarning("Username is not an inspector\'s username",
                                   "The username you entered is not an inspector\'s username.")
            return False
        usernameAndPasswordMatch = self.cursor.execute(
            "SELECT * FROM registereduser WHERE (username = %s AND password = %s)", (username, password))
        if not usernameAndPasswordMatch:
            messagebox.showwarning("Username and password don\'t match", "Sorry, the username and password you entered"
                                                                         + " do not match.")
            return False
        self.loginWindow.withdraw()
        inspector = Inspector()
        return True

    def connect(self):
        try:
            db = pymysql.connect(host = 'academic-mysql.cc.gatech.edu',
                                 db = 'cs4400_Group_24', user = 'cs4400_Group_24', passwd = 'jGZgXJfO')
            return db
        except:
            messagebox.showwarning('Error!','Cannot connect. Please check your internet connection.')
            return False

a = RestaurantInspectionApp()
