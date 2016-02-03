
from tkinter import *
import pymysql
from tkinter import messagebox
class Guest(object):
    def __init__(self):
        self.db = self.connect()
        self.cursor = self.db.cursor()

        #Guest Menu Window
        self.guestMenuWindow = Toplevel()
        self.guestMenuWindow.title("Georgia Restaurant Health Inspections - Guest Menu")

        # Guest Search Restaurants Window
        self.restaurantSearchWindow = Toplevel()
        self.restaurantSearchWindow.title("Georgia Restaurant Health Inspections - Search for Restaurants")
        self.restaurantSearchWindow.withdraw()

        # Guest Search Restaurant Result Window
        self.restaurantSearchResultWindow = Toplevel()
        self.restaurantSearchResultWindow.title("Georgia Restaurant Health Inspections - Search for Restaurants")
        self.restaurantSearchResultWindow.withdraw()

        #Guest File Cmplaint Window
        self.fileComplaintWindow = Toplevel()
        self.fileComplaintWindow.title("Georgia Restaurant Health Inspections - File a Complaint")
        self.fileComplaintWindow.withdraw()

        self.buildGuestMenuWindow()
        self.guestMenuWindow.mainloop()

    def buildGuestMenuWindow(self):
        guestMenuWindow = self.guestMenuWindow
        searchRestaurantsButton = Button(guestMenuWindow, text = "Search for Restaurants", command = self.searchRestaurantsButtonClicked)
        searchRestaurantsButton.grid(row = 1, column = 1, sticky = W + E)

        fileComplaintButton = Button(guestMenuWindow, text = "File a Complaint", command = self.fileComplaintButtonClicked)
        fileComplaintButton.grid(row = 1, column = 2, sticky = W + E)

        exitSystemButton = Button(guestMenuWindow, text = "Exit the System", command = self.exitSystemButtonClicked)
        exitSystemButton.grid(row = 1, column = 3, sticky = W + E)

    def searchRestaurantsButtonClicked(self):
        self.guestMenuWindow.withdraw()
        self.buildSearchRestaurantWindow(self.restaurantSearchWindow)
        self.restaurantSearchWindow.deiconify()

    def fileComplaintButtonClicked(self):
        self.guestMenuWindow.withdraw()
        self.buildFileComplaintWindow(self.fileComplaintWindow)
        self.fileComplaintWindow.deiconify()

    def exitSystemButtonClicked(self):
        self.guestMenuWindow.destroy()

    def buildSearchRestaurantWindow(self, window):
        # Search Button
        restaurantSearchButton = Button(window, text="Restaurant Search",
                                        command = self.searchRestaurantButtonClicked_infoSubmitted)
        restaurantSearchButton.grid(row = 1, column = 2, sticky = W)

        # Create Labels and Entries
        labelTextList = ["Name", "Score*", "Zipcode*", "Cuisine"]
        self.searchCriteriaList = []
        searchCriteriaEntryList = []
        for i in range(len(labelTextList)):
            Label(window, text = labelTextList[i]).grid(row = 2 + i, column = 2, sticky = W + E)
            if i != 3:
                (searchCriteria, searchCriteriaEntry) = self.createAnEntry(2 + i, 4, 30, window)
                self.searchCriteriaList.append(searchCriteria)
                searchCriteriaEntryList.append(searchCriteriaEntry)
        # Add Cuisine Dropdown Menu
        self.cuisineChoice = StringVar()
        self.cuisineChooseFromList = []
        self.cursor.execute("SELECT cuisine FROM cuisines")
        cuisineTuple = self.cursor.fetchall()
        for i in cuisineTuple:
            self.cuisineChooseFromList.append(i[0])
        OptionMenu(window, self.cuisineChoice, *self.cuisineChooseFromList).grid(row = 5, column = 4, sticky = W + E)

        # Add Score > or <
        self.compareChoice = StringVar()
        self.compareChoiceChooseFromList = ["<", ">"]
        OptionMenu(window, self.compareChoice, *self.compareChoiceChooseFromList).\
            grid(row = 3, column = 3, sticky = W + E)

        # Required Condition
        requiredCondition = Label(window, text="* Required Condition", bg="gold")
        requiredCondition.grid(row=6, column=2, sticky=W)

        # Back Button
        backButton = Button(window, text = "Back", command = self.restaurantSearchBackButtonClicked)
        backButton.grid(row = 1, column = 1, sticky = E)


    def restaurantSearchBackButtonClicked(self):
        self.restaurantSearchWindow.withdraw()
        self.guestMenuWindow.deiconify()

    def searchRestaurantButtonClicked_infoSubmitted(self):
        score = self.searchCriteriaList[1].get()
        zipcode = self.searchCriteriaList[2].get()
        if not score:
            messagebox.showwarning("Error!","Must enter minimum score.")
            return False
        if not zipcode:
            messagebox.showwarning("Error!", "Must enter zipcode.")
            return False
        try:
            self.searchRestaurant(self.searchCriteriaList[0].get(),
                              score, zipcode, self.cuisineChoice.get(), self.restaurantSearchResultWindow,
                              self.gridList)
        except:
            self.searchRestaurant(self.searchCriteriaList[0].get(),
                              score, zipcode, self.cuisineChoice.get(), self.restaurantSearchResultWindow,
                              [])
        return True

    def buildFileComplaintWindow(self, window):
        # Title Label
        titleLabel = Label(window, text = "Food/Safety Complaint")
        titleLabel.grid(row =1, column = 1, sticky = W + E)

        #Create Labels and Entries
        labelTextList = ["Restaurant", "Date of Meal, yyyy-mm-dd",
                         "Customer First Name", "Customer Last Name",
                         "Customer Phone", "Complaint Description"]
        self.complaintInfoList = []
        complaintInfoEntryList = []
        for i in range(len(labelTextList)):
            Label(window, text = labelTextList[i]).grid(row = 2 + i, column = 1, sticky = W + E)
            if i != 0:
                (info, infoEntry) = self.createAnEntry(2 + i, 2, 30, window)
                self.complaintInfoList.append(info)
                complaintInfoEntryList.append(infoEntry)
            else:
                self.cursor.execute("SELECT name, street, city, state, zipcode FROM restaurant")
                self.restaurantList = []
                restaurantTuple = self.cursor.fetchall()
                for i in restaurantTuple:
                    restaurantString = ""
                    for j in range(len(i)):
                        if j == 0:
                            restaurantString += i[j]
                        else:
                            restaurantString = restaurantString + ', ' + str(i[j])
                    self.restaurantList.append(restaurantString)
                self.restaurantChoice = StringVar()
                self.complaintInfoList.append(self.restaurantChoice)
                restaurantOptionMenu = OptionMenu(window, self.restaurantChoice, *self.restaurantList)
                restaurantOptionMenu.grid(row = 2, column = 2, sticky = W + E)
        # Submit Button
        submitButton = Button(window, text = "Submit", command = self.submitComplaintButtonClicked)
        submitButton.grid(row = 11, column = 1)
        # Back Button
        Button(window, text = "Back", command = self.backFromFileComplaintWindowToMainMenu).grid(row = 11, column = 2)

    def backFromFileComplaintWindowToMainMenu(self):
        self.fileComplaintWindow.withdraw()
        self.guestMenuWindow.deiconify()

    def searchRestaurant(self, name, score, zipcode, cuisine, window, gridList):
        # Clear Window
        for i in range(len(gridList)):
            for j in range(len(self.gridList[i])):
                Label(window, text = self.gridList[i][j]).grid(row = 2 + j, column = i + 1, sticky = W + E)
        # Get all restaurant name and rid by zipcode
        if not self.cursor.execute("SELECT name, rid FROM restaurant WHERE zipcode = %s GROUP BY rid", zipcode):
            messagebox.showwarning("Can not find", "Can not find a restaurant matching your search criteria.")
            return False
        else:
            resultByZipcodeTuple = self.cursor.fetchall()
            resultList = []
            for i in resultByZipcodeTuple:
                sublist = []
                for j in i:
                    sublist.append(j)
                resultList.append(sublist)

            # From the restaurant matching provided zipcode, select those matching score
            copyResultList = []
            for i in resultList:
                copyResultList.append(i)
            for i in range(len(copyResultList)):
                print(self.compareChoice.get())
                if self.compareChoice.get() == "<":
                    scoreSearchResult = self.cursor.execute("SELECT street, city, state, zipcode, cuisine, totalscore, idate FROM restaurant NATURAL JOIN inspection WHERE totalscore < %s and restaurant.rid = %s GROUP BY idate ORDER BY idate DESC",
                                                        (score, resultList[i][1]))
                else:
                    scoreSearchResult = self.cursor.execute("SELECT street, city, state, zipcode, cuisine, totalscore, idate FROM restaurant NATURAL JOIN inspection WHERE totalscore > %s and restaurant.rid = %s GROUP BY idate ORDER BY idate DESC",
                                                        (score, resultList[i][1]))
                if not scoreSearchResult:
                    resultList.remove(copyResultList[i])
                else:
                    restaurantInfoTuple = self.cursor.fetchone()
                    address = restaurantInfoTuple[0] + ", " + restaurantInfoTuple[1] + \
                              ", " + restaurantInfoTuple[2] + " " + str(restaurantInfoTuple[3])
                    resultList[i] += [address, restaurantInfoTuple[4], restaurantInfoTuple[5], restaurantInfoTuple[6].strftime('%m/%d/%Y')]
            if not resultList:
                messagebox.showwarning("Can not find", "Can not find any restaurant matching your search criteria.")
                return False

            # Check if restaurant name is entered
            copyResultList = []
            for i in resultList:
                copyResultList.append(i)
            if name:
                name.lower()
                for i in range(len(copyResultList)):
                    if not (name in copyResultList[i][0].lower()):
                        resultList.remove(copyResultList[i])
                if not resultList:
                    messagebox.showwarning("Can not find", "Can not find a restaurant matching your search criteria.")
                    return False
            # Check if cuisine is entered
            copyResultList = []
            for i in resultList:
                copyResultList.append(i)
            if cuisine:
                for i in range(len(copyResultList)):
                    if not (cuisine in copyResultList[i]):
                        resultList.remove(copyResultList[i])
                if not resultList:
                    messagebox.showwarning("Can not find", "Can not find a restaurant matching your search criteria.")
                    return False

            # Grid Results
            self.restaurantNameList = ["Restaurant Name"]
            self.addressList = ["Address"]
            self.cuisineList = ["Cuisine"]
            self.scoreList = ["Last Inspection Score"]
            self.dateList = ["Date Of Last Inspection"]
            for i in resultList:
                self.restaurantNameList.append(i[0])
                self.addressList.append(i[2])
                self.cuisineList.append(i[3])
                self.scoreList.append(i[4])
                self.dateList.append(i[5])
            self.gridList = [self.restaurantNameList, self.addressList, self.cuisineList, self.scoreList, self.dateList]
            for i in range(len(self.gridList)):
                for j in range(len(self.gridList[i])):
                    Label(window, text = self.gridList[i][j]).grid(row = 2 + j, column = i + 1, sticky = W + E)
            for i in range(len(self.gridList)):
                for j in range(len(self.gridList[i])):
                    self.gridList[i][j] = "            "
            # Back button
            Button(window, text = "Back", command = self.backToSearchRestaurantWindow).grid(row = 1, column = 1, sticky = W)

            self.restaurantSearchWindow.withdraw()
            self.restaurantSearchResultWindow.deiconify()



    def backToSearchRestaurantWindow(self):
        self.restaurantSearchResultWindow.withdraw()
        self.restaurantSearchWindow.deiconify()

    def submitComplaintButtonClicked(self):
        #submit the complaint to database
        restaurant = self.complaintInfoList[0].get().split(',')[0]
        self.cursor.execute("SELECT rid FROM restaurant WHERE name = %s", restaurant)
        restaurantID = self.cursor.fetchone()[0]
        phone = self.complaintInfoList[4].get()
        cdate = self.complaintInfoList[1].get()
        customerFirstName = self.complaintInfoList[2].get()
        customerLastName = self.complaintInfoList[3].get()
        '''
        address = self.complaintInfoList[0].get().split(', ', 1)[1]
        print("address: " + address)
        self.cursor.execute("SELECT email FROM restaurant WHERE name = %s", restaurant)
        operatorEmail = self.cursor.fetchone()[0]
        print("email: " + operatorEmail)
        self.cursor.execute("SELECT firstname, lastname FROM operatorowner WHERE email = %s", operatorEmail)
        nameTuple = self.cursor.fetchall()
        operatorName = nameTuple[0][0] + ' ' + nameTuple[0][1]
        print(operatorName)
        self.cursor.execute("SELECT totalscore FROM inspection WHERE rid = %s ORDER BY idate DESC", restaurantID)
        score = self.cursor.fetchone()[0]
        print("score: " + str(score))
        '''
        complaint = self.complaintInfoList[-1].get()
        result = self.cursor.execute("SELECT * FROM customer WHERE phone = %s", phone)
        if not result:
            self.cursor.execute("INSERT INTO customer (phone, firstname, lastname) VALUES (%s, %s, %s)",
                            (phone, customerFirstName, customerLastName))
            self.db.commit()
        self.cursor.execute("INSERT INTO complaint (rid, phone, cdate, description) VALUES (%s, %s, %s, %s)",
                            (restaurantID, phone, cdate, complaint))
        self.db.commit()
        messagebox.showwarning("Submission Successful!", "Your complaint has been submitted.")
        self.fileComplaintWindow.withdraw()
        self.guestMenuWindow.deiconify()

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