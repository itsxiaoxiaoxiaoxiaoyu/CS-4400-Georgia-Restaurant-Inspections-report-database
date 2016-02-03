from tkinter import *
import pymysql
import random
from tkinter import messagebox
class Operator(object):

    def __init__(self, username):
        self.username = username
        self.db = self.connect()
        self.cursor = self.db.cursor()
        self.cursor.execute("SELECT email FROM operatorowner WHERE username = %s", self.username)
        self.email = self.cursor.fetchone()[0]
        # Operator's Menu
        self.operatorMenuWindow = Tk()
        self.operatorMenuWindow.title("Georgia Restaurant Health Inspections - Operator\'s Menu")

        # Enter Restaurant Info Window
        self.enterInfoWindow = Toplevel()
        self.enterInfoWindow.title("Georgia Restaurant Health Inspections - Enter Restaurant Information")
        self.enterInfoWindow.withdraw()

        # Display Report Window
        # This may not be a good naming though... the display report window is actually
        # the window in which we enter search restaurant criteria
        self.displayReportWindow = Toplevel()
        self.displayReportWindow.title("Georgia Restaurant Health Inspections - Search for a Report")
        self.displayReportWindow.withdraw()

        # Generate Report Window
        # This is the actual window in which reports are displayed
        self.generateReportWindow = Toplevel()
        self.generateReportWindow.title("Georgia Restaurant Health Inspections - Display Health Inspection Report Results")
        self.generateReportWindow.withdraw()

        self.buildOperatorMenuWindow(self.operatorMenuWindow)
        self.operatorMenuWindow.mainloop()

#-----------------------------------BUTTON CLICKED METHODS------------------------------------

    def enterInfoButtonClicked(self):
        self.operatorMenuWindow.withdraw()
        self.buildEnterInfoWindow(self.enterInfoWindow)
        self.enterInfoWindow.deiconify()

    def displayReportButtonClicked(self):
        self.operatorMenuWindow.withdraw()
        self.buildDisplayReportWindow(self.displayReportWindow)
        self.displayReportWindow.deiconify()

    def exitSystemButtonClicked(self):
        self.operatorMenuWindow.destroy()

    def submitRestaurantInfoButtonClicked(self):
        #Submit entered information to the restaurant table
        restaurantID = self.generateRestaurantID()
        infoList = ["Health Permit ID", "Health Permit Expiration Date yyyy-mm-dd",
                         "Cuisine", "Restaurant Name", "Street", "City", "State", "Zipcode", "County",
                         "Restaurant Phone"]
        infoDictionary = {}
        for i in range(10):
            if i != 2:
                if i < 2:
                    infoDictionary[infoList[i]] = self.enterInfoList[i].get()
                else:
                    infoDictionary[infoList[i]] = self.enterInfoList[i-1].get()
            else:
                infoDictionary[infoList[i]] = self.cuisineChoice.get()

        #Check if all entries are filled.
        for i in range(len(self.enterInfoList)):
            if not self.enterInfoList[i].get():
                messagebox.showwarning("Empty input", "Please fill in all entries.")
                return False

        # See if cuisine already exists. If not, add into the cuisines table.
        self.cursor.execute("SELECT cuisine FROM cuisines")
        cuisineTuple = self.cursor.fetchall()
        cuisineList = []
        for i in cuisineTuple:
            cuisineList.append(i[0])
        cuisine = infoDictionary["Cuisine"]
        if not (infoDictionary["Cuisine"] in cuisineList):
            self.cursor.execute('INSERT INTO cuisines (cuisine) VALUES (%s)',cuisine)
            self.db.commit()
        # Insert info into the restaurant table
        insertInfoQuery = 'INSERT INTO restaurant (rid, phone, name, county, street, city, state, zipcode, cuisine, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        result = self.cursor.execute(insertInfoQuery,
                            (restaurantID, infoDictionary["Restaurant Phone"], infoDictionary["Restaurant Name"],
                             infoDictionary["County"], infoDictionary["Street"], infoDictionary["City"],
                             infoDictionary["State"], infoDictionary["Zipcode"],
                             infoDictionary["Cuisine"], self.email))
        self.db.commit()
        insertInfoQuery = 'INSERT INTO healthpermit(hpid, expirationdate, rid) VALUES (%s, %s, %s)'
        result = self.cursor.execute(insertInfoQuery, (infoDictionary["Health Permit ID"], infoDictionary["Health Permit Expiration Date yyyy-mm-dd"], restaurantID))
        self.db.commit()
        messagebox.showwarning("Restaurant Info Submission Successful", "Submission successful. Your restaurant ID is: " + str(restaurantID))
        self.enterInfoWindow.withdraw()
        self.operatorMenuWindow.deiconify()
        return True

    def searchButtonClicked(self):
        if not self.restaurantIDChoice.get():
            messagebox.showwarning("Empty restaurant ID input", "Please select restaurant ID.")
            return False
        if not self.restaurantNameChoice.get():
            messagebox.showwarning("Empty restaurant name input", "Please select restaurant name.")
            return False
        if not self.addressChoice.get():
            messagebox.showwarning("Empty address input", "Please select restaurant address.")
            return False
        # Check if the choices match (as one restaurant)
        street = self.addressChoice.get().split(",")[0]
        result = self.cursor.execute("SELECT * FROM restaurant WHERE (rid = %s AND name = %s AND street = %s AND email = %s)",
                            (int(self.restaurantIDChoice.get()),
                             self.restaurantNameChoice.get(), street, self.email))
        if not result:
            messagebox.showwarning("Error", "The restaurant ID, name and address you selected do not match.")
            return False
        self.displayReportWindow.withdraw()
        self.buildGenerateReportWindow(self.restaurantIDChoice.get(),
                                       self.restaurantNameChoice.get(),
                                       self.addressChoice.get(),
                                       self.generateReportWindow)
        self.generateReportWindow.deiconify()

#------------------------------------BUILD WINDOW METHODS------------------------------------------------

    def buildOperatorMenuWindow(self, window):
        # Enter Restaurant Info Button
        enterInfoButton = Button(window, text = "Enter Restaurant Information", command = self.enterInfoButtonClicked)
        enterInfoButton.grid(row = 1, column = 1, sticky = W + E)

        # Display Report Results
        displayReportButton = Button(window,
                                     text = "Display Health Inspection Report Results",
                                     command = self.displayReportButtonClicked)
        displayReportButton.grid(row = 1, column = 2, sticky = W + E)

        # Exit System Button
        exitSystem = Button(window, text = "Exit System", command = self.exitSystemButtonClicked)
        exitSystem.grid(row = 1, column = 3, sticky = W + E)

    def buildEnterInfoWindow(self, window):
        # Title Label
        enterInfoLabel = Label(window, text = "Enter All Information")
        enterInfoLabel.grid(row = 1, column = 1, sticky = W + E)

        # Create Labels and Entries
        labelTextList = ["Health Permit ID", "Health Permit Expiration Date yyyy-mm-dd",
                         "Cuisine", "Restaurant Name", "Street", "City", "State", "Zipcode", "County",
                         "Restaurant Phone"]
        self.enterInfoList = []
        enterInfoEntryList = []
        for i in range(len(labelTextList)):
            Label(window, text = labelTextList[i]).grid(row = 2 + i, column = 1, sticky = W + E)
            if i != 2:
                (enterInfo, enterInfoEntry) = self.createAnEntry(2 + i, 2, 30, window)
                self.enterInfoList.append(enterInfo)
                enterInfoEntryList.append(enterInfoEntry)
        # Cuisine Option Menu
        # Add Cuisine Dropdown Menu
        self.cuisineChoice = StringVar()
        self.cuisineChooseFromList = []
        self.cursor.execute("SELECT cuisine FROM cuisines")
        cuisineTuple = self.cursor.fetchall()
        for i in cuisineTuple:
            self.cuisineChooseFromList.append(i[0])
        OptionMenu(window, self.cuisineChoice, *self.cuisineChooseFromList).grid(row = 4, column = 2, sticky = W + E)


        # Submit Button
        submitRestaurantInfoButton = Button(window, text = "Submit", command = self.submitRestaurantInfoButtonClicked)
        submitRestaurantInfoButton.grid(row = 13, column = 1, sticky = W)

    def buildDisplayReportWindow(self, window):
        # Back Button
        backButton = Button(window, text = "Back", command = self.backFromDisplayReportWindowToOperatorMenu)
        backButton.grid(row = 1, column = 2, sticky = E)

        # Select Search Criteria Label
        selectSearchCriteriaLabel = Label(window, text = "Select Search Criteria")
        selectSearchCriteriaLabel.grid(row = 1, column = 1, sticky = W)

        # Restaurant ID Label
        restaurantIDLabel = Label(window, text = "Restaurant ID")
        restaurantIDLabel.grid(row = 2, column = 1, sticky = W + E)

        # Get restaurant ID, name, address list from the database
        self.restaurantIDList = []
        self.restaurantNameList = []
        self.restaurantAddressList = []
        self.cursor.execute("SELECT rid FROM restaurant WHERE email = %s", self.email)
        restaurantIDTuple = self.cursor.fetchall()
        for i in restaurantIDTuple:
            self.restaurantIDList.append(i[0])
        self.cursor.execute("SELECT name FROM restaurant WHERE email = %s", self.email)
        restaurantNameTuple = self.cursor.fetchall()
        for i in restaurantNameTuple:
            self.restaurantNameList.append(i[0])
        self.cursor.execute("SELECT street, city, state, zipcode FROM restaurant WHERE email = %s", self.email)
        restaurantAddressTuple = self.cursor.fetchall()
        for i in restaurantAddressTuple:
            address = ""
            for j in i:
                address  = address + str(j) + ", "
            address = address[0:len(address)-2]
            self.restaurantAddressList.append(address)
        # Restaurant ID Dropdown
        self.restaurantIDChoice = StringVar()
        restaurantIDOptionMenu = OptionMenu(window, self.restaurantIDChoice, *self.restaurantIDList)
        restaurantIDOptionMenu.grid(row = 2, column = 2, sticky = W + E)

        # Restaurant Name Label
        restaurantNameLabel = Label(window, text = "Restaurant Name")
        restaurantNameLabel.grid(row = 3, column = 1, sticky = W + E)
        # Restaurant Name Dropdown
        self.restaurantNameChoice = StringVar()
        restaurantNameOptionMenu = OptionMenu(window, self.restaurantNameChoice, *self.restaurantNameList, command = self.restaurantNameSelected)
        restaurantNameOptionMenu.grid(row = 3, column = 2, sticky = W + E)

        # Address Label
        addressLabel = Label(window, text = "Address")
        addressLabel.grid(row = 4, column = 1, sticky = W + E)
        # Address Dropdown
        self.addressChoice = StringVar()
        addressOptionMenu = OptionMenu(window, self.addressChoice, *self.restaurantAddressList)
        addressOptionMenu.grid(row = 4, column = 2, sticky = W + E)

        #Search Button
        searchButton = Button(window, text = "Search", command = self.searchButtonClicked)
        searchButton.grid(row = 5, column = 1, sticky = W + E)

    def buildGenerateReportWindow(self, ID, name, address, window):
        # Back Button
        backButton = Button(window, text = "back", command = self.backToSearchCriteriaWindow)
        backButton.grid(row = 1, column = 2, sticky = E)

        # Inspection Results Label
        inspectionResultsLabel = Label(window, text = "Inspection Results")
        inspectionResultsLabel.grid(row = 1, column = 1, sticky = W)

        # Display item number and description
        self.cursor.execute("SELECT * FROM item")
        itemTuple = self.cursor.fetchall()
        itemNumberList = ["Item Number"]
        itemDescriptionList = ["Item Description"]
        for i in itemTuple:
            itemNumberList.append(str(i[0]))
            itemDescriptionList.append(str(i[2]))
        # Grid all item numbers
        for i in range(len(itemNumberList)):
            Label(window, text = itemNumberList[i]).grid(row = 2 + i, column = 1, sticky = W)
        # Grid all the item descriptions
        for i in range(len(itemDescriptionList)):
            Label(window, text = itemDescriptionList[i], width = 100).grid(row = 2 + i,
                                                                          column = 2, columnspan = 3, sticky = W)
        rid = int(self.restaurantIDChoice.get())
        self.cursor.execute("SELECT DISTINCT idate FROM contains WHERE rid = %s ORDER BY idate DESC", rid)
        datesTuple = self.cursor.fetchall()
        length = len(datesTuple)
        for i in range(2):
            try:
                Label(window, text = "Score on " + str(datesTuple[i][0].strftime('%m/%d/%Y'))).grid(row = 2, column = 5 + i, sticky = E)
                self.cursor.execute("SELECT itemnum, score FROM contains WHERE rid = %s AND idate = %s ORDER BY itemnum ASC", (rid, datesTuple[i][0]))
                itemNumAndScoreTuple = self.cursor.fetchall()
                for j in range(len(itemNumAndScoreTuple)):
                    score = itemNumAndScoreTuple[j][1]
                    if (j in range(0, 8)) and score < 8:
                        Label(window, text = str(score), bg = "light green").grid(row = 3 + j, column = 5 + i, sticky = E)
                    else:
                        Label(window, text = str(score)).grid(row = 3 + j, column = 5 + i, sticky = E)
                    if j == len(itemNumAndScoreTuple) - 1:
                        # Total Score
                        self.cursor.execute("SELECT SUM(score) AS 'sumScore' FROM contains WHERE idate = %s AND rid = %s", (datesTuple[i][0], rid))
                        sumScore = self.cursor.fetchone()[0]
                        Label(window, text = "Total: " + str(sumScore)).grid(row = 4 + j, column = 5 + i, sticky = E)
                        # Final Result
                        self.cursor.execute("SELECT passfail FROM inspection WHERE idate = %s AND rid = %s", (datesTuple[i][0], rid))
                        passOrFail = self.cursor.fetchone()[0]
                        if passOrFail == "PASS":
                            Label(window, text = "Result: " + passOrFail).grid(row = 5 + j, column = 5 + i, sticky = E)
                        else:
                            Label(window, text = "Result: " + passOrFail, bg = "light green").grid(row = 5 + j, column = 5 + i, sticky = E)

            except:
                break








#---------------------------------BACK BUTTON ASSOCIATED METHODS------------------------
    def backFromDisplayReportWindowToOperatorMenu(self):
        self.displayReportWindow.withdraw()
        self.operatorMenuWindow.deiconify()

    def backToSearchCriteriaWindow(self):
        self.generateReportWindow.withdraw()
        self.displayReportWindow.deiconify()

#------------------------HELPER METHODS----------------------------------------------

    def restaurantNameSelected(self, event):
        self.restaurantNameChoice.get()

    def generateRestaurantID(self):
        restaurantID = random.getrandbits(9);
        result = self.cursor.execute("SELECT rid FROM restaurant WHERE rid = %s", restaurantID)

        while result:
            restaurantID = random.getrandbits(9);
        return restaurantID

    def createAnEntry(self, rowNumber, columnNumber, widthNumber, window):
        aStringVar = StringVar()
        anEntry = Entry(window, textvariable = aStringVar, width = widthNumber)
        anEntry.grid(row = rowNumber, column = columnNumber, sticky = W + E)
        return aStringVar, anEntry

    def connect(self):
        try:
            db = pymysql.connect(host = 'academic-mysql.cc.gatech.edu',
                                 db = 'cs4400_Group_24', user = 'cs4400_Group_24', passwd = 'jGZgXJfO')
            return db
        except:
            messagebox.showwarning('Error!','Cannot connect. Please check your internet connection.')
            return False