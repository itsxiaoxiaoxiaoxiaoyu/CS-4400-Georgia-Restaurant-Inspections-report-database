from tkinter import *
import pymysql
from tkinter import messagebox
class Inspector(object):
    def __init__(self):
        self.db = self.connect()
        self.cursor = self.db.cursor()
        # Inspector's Menu Window
        self.inspectorMenuWindow = Tk()
        self.inspectorMenuWindow.title("Georgia Restaurant Health Inspections - Inspector\'s Menu")

        # Insert Restaurant Inspection Report Window
        self.insertReportWindow = Toplevel()
        self.insertReportWindow.title("Georgia Restaurant Health Inspections - Insert a Restaurant Inspection Report")
        self.insertReportWindow.withdraw()

        # View Reports Criteria Window
        self.viewReportsCriteriaWindow = Toplevel()
        self.viewReportsCriteriaWindow.title("Georgia Restaurant Health Inspections -"
                                             + "View Summary of Restaurant Inspection Reports")
        self.viewReportsCriteriaWindow.withdraw()

        # View Reports By Month And Year Window
        self.viewReportsByMonthAndYearWindow = Toplevel()
        self.viewReportsByMonthAndYearWindow.title("Georgia Restaurant Health Inspections -"
                                                   + "View Report By Month And Year")
        self.viewReportsByMonthAndYearWindow.withdraw()

        # View Reports By Month And Year For a Specified County Window
        self.viewReportsByMonthAndYearForACountyWindow = Toplevel()
        self.viewReportsByMonthAndYearForACountyWindow.title("Georgia Restaurant Health Inspections -"
                                                             + "View Report By Month And Year For A Specified County")
        self.viewReportsByMonthAndYearForACountyWindow.withdraw()

        # View Top Restaurant by Cuisine For a Year and County Window
        self.viewTopRestaurantByCuisineForAYearAndCountyWindow = Toplevel()
        self.viewTopRestaurantByCuisineForAYearAndCountyWindow.title("Georgia Restaurant Health Inspections -"
                                                                     + "View Top Restaurant by "
                                                                     + "Cuisine For a Year and County")
        self.viewTopRestaurantByCuisineForAYearAndCountyWindow.withdraw()

        # View Restaurants With Complaints Window
        self.viewRestaurantsWithComplaintsWindow = Toplevel()
        self.viewRestaurantsWithComplaintsWindow.title("Georgia Restaurant Health Inspections -"
                                                       + "View Restaurants With Complaints"
                                                       + " (At least one nonperfect critical item score on inspection)")
        self.viewRestaurantsWithComplaintsWindow.withdraw()

        self.buildInspectorMenu(self.inspectorMenuWindow)
        self.inspectorMenuWindow.mainloop()

#-----------------------BUILD INSPECTOR MENU METHOD-------------------------------------------------

    def buildInspectorMenu(self, window):
        # Insert Restaurant Inspection Report Button
        insertReportButton = Button(window, text = "Insert a Restaurant Inspection Report",
                                    command = self.insertReportButtonClicked)
        insertReportButton.grid(row = 1, column = 1, sticky = W + E)

        # Display 4 Summary Reports Button
        displayReportsButton = Button(window, text = "Display 4 Summary Reports",
                                      command = self.displayReportsButtonClicked)
        displayReportsButton.grid(row = 1, column = 2, sticky = W + E)

        # Exit System Button
        exitSystemButton = Button(window, text = "Exit System", command = self.exitSysemButtonClicked)
        exitSystemButton.grid(row = 1, column = 3, sticky = W + E)

#------------INSPECTOR MENU BUTTON CLICKED METHODS--------------------------------------------------

    def insertReportButtonClicked(self):
        self.inspectorMenuWindow.withdraw()
        self.buildInsertReportWindow(self.insertReportWindow)
        self.insertReportWindow.deiconify()

    def displayReportsButtonClicked(self):
        self.inspectorMenuWindow.withdraw()
        self.buildViewReportsCriteriaWindow(self.viewReportsCriteriaWindow)
        self.viewReportsCriteriaWindow.deiconify()

    def exitSysemButtonClicked(self):
        self.inspectorMenuWindow.destroy()

#-------------------BUILD VIEW REPORTS BY 4 CRITERIA WINDOW METHOD-------------------------------------

    def buildViewReportsCriteriaWindow(self, window):
        Button(window, text = "Summary by Month and Year", width = 40,
               command = self.viewReportsByMonthAndYearButtonClicked).grid(row = 1, column = 1, sticky = W + E)
        Button(window, text = "Summary by Month and Year for a Specified County", width = 40,
               command = self.viewReportsByMonthAndYearForACountyButtonClicked).\
            grid(row = 2, column = 1, sticky = W + E)
        Button(window, text = "Top Restaurant by Cuisine for a Year/County", width = 40,
               command = self.topRestaurantByCuisineForAYearAndCountyButtonClicked).\
            grid(row = 3, column = 1, sticky = W + E)
        Button(window, text = "Restaurants with Complaints", width = 40,
               command = self.restaurantsWithComplaintsButtonClicked).grid(row = 4, column = 1, sticky = W + E)
        Button(window, text = "Back", command = self.backFromViewReportsCriteriaWindow).\
            grid(row = 5, column = 1, sticky = W + E)

#----------------VIEW REPORTS BY 4 CRITERIA BUTTON CLICKED METHODS--------------------------------------------

    def viewReportsByMonthAndYearButtonClicked(self):
        self.viewReportsCriteriaWindow.withdraw()
        self.buildViewReportsByMonthAndYearWindow(self.viewReportsByMonthAndYearWindow)
        self.viewReportsByMonthAndYearWindow.deiconify()

    def viewReportsByMonthAndYearForACountyButtonClicked(self):
        self.viewReportsCriteriaWindow.withdraw()
        self.buildViewReportsByMonthAndYearForACountyWindow(self.viewReportsByMonthAndYearForACountyWindow)
        self.viewReportsByMonthAndYearForACountyWindow.deiconify()

    def topRestaurantByCuisineForAYearAndCountyButtonClicked(self):
        self.viewReportsCriteriaWindow.withdraw()
        self.buildViewtopRestaurantByCuisineForAYearAndCountyWindow\
            (self.viewTopRestaurantByCuisineForAYearAndCountyWindow)
        self.viewTopRestaurantByCuisineForAYearAndCountyWindow.deiconify()

    def restaurantsWithComplaintsButtonClicked(self):
        self.viewReportsCriteriaWindow.withdraw()
        self.buildViewRestaurantsWithComplaintsWindow(self.viewRestaurantsWithComplaintsWindow)
        self.viewRestaurantsWithComplaintsWindow.deiconify()

#-------------------BUILD VIEW REPORT BY 4 CRITERIA WINDOW METHODS----------------------------------

    def buildViewReportsByMonthAndYearWindow(self, window):
        # Back Button
        Button(window, text = "Back", command = self.backFromViewReportsByMonthAndYearWindowToInspectorMenu).\
            grid(row = 1, column = 1, sticky = W + E)

        # Enter Month Label
        Label(window, text = "Enter Month: mm").grid(row = 1, column = 2, sticky = W + E)

        # Enter Month Entry
        self.monthOfReportByMonthAndYear = StringVar()
        Entry(window, textvariable = self.monthOfReportByMonthAndYear,
              width = 30).grid(row = 1, column = 3, sticky = W + E)

        # Enter Year Label
        Label(window, text = "Enter Year: yyyy").grid(row = 1, column = 4, sticky = W + E)

        # Enter Year Entry
        self.yearOfReportByMonthAndYear = StringVar()
        Entry(window, textvariable = self.yearOfReportByMonthAndYear,
              width = 30).grid(row = 1, column = 5, sticky = W + E)

        # View Button
        Button(window, text = "View", command = self.viewReportsByMonthAndYearButtonClicked_infoSubmitted).\
            grid(row = 1, column = 6, sticky = W + E)

        # Column Lists
        labelTextList = ["County", "Cuisine", "Number of Restaurants Inspected", "Number of Restaurants Failed"]
        columnList = [1, 2, 3, 4]
        for i in columnList:
            Label(window, text = labelTextList[i-1]).grid(row = 2, column = i, sticky = W + E)

    def buildViewReportsByMonthAndYearForACountyWindow(self, window):
        # Back Button
        Button(window, text = "Back", command = self.backFromViewReportsByMonthAndYearForACountyWindowToInspectorMenu)\
            .grid(row = 1, column = 1, sticky = W + E)

        # Enter Year Label
        Label(window, text = "Enter Year: yyyy").grid(row = 1, column = 2, sticky = W + E)

        # Enter Year Entry
        self.yearOfReportByYearAndCounty = StringVar()
        Entry(window, textvariable = self.yearOfReportByYearAndCounty, width = 30).\
            grid(row = 1, column = 3, sticky = W + E)

        # Enter County Label
        Label(window, text = "Enter County").grid(row = 1, column = 4, sticky = W + E)

        # Enter County Entry
        self.countyInspectedByYearAndCounty = StringVar()
        Entry(window, textvariable = self.countyInspectedByYearAndCounty, width = 30).\
            grid(row = 1, column = 5, sticky = W + E)

        # View Button
        Button(window, text = "View", command = self.viewReportsByMonthAndYearForACountyButtonClicked_infoSubmitted).\
            grid(row = 1, column = 6, sticky = W + E)

    def buildViewtopRestaurantByCuisineForAYearAndCountyWindow(self, window):
        # Back Button
        Button(window, text = "Back",
               command = self.backFromViewtopRestaurantByCuisineForAYearAndCountyWindowToInspectorMenuWindow).\
        grid(row = 1, column = 1, sticky = W + E)

        # Enter Year Label
        Label(window, text = "Enter Year: yyyy").grid(row = 1, column = 2, sticky = W + E)

        # Enter Year Entry
        self.yearOfReport_topRestaurant = StringVar()
        Entry(window, textvariable = self.yearOfReport_topRestaurant, width = 30).\
            grid(row = 1, column = 3, sticky = W + E)

        # Enter County Label
        Label(window, text = "Enter County").grid(row = 1, column = 4, sticky = W + E)

        # Enter County Entry
        self.countyInspected_topRestaurant = StringVar()
        Entry(window, textvariable = self.countyInspected_topRestaurant, width = 30).\
            grid(row = 1, column = 5, sticky = W + E)

        # View Button
        Button(window, text = "View",
               command = self.viewTopRestaurantByCuisineForAYearAndCountyButtonClicked_infoSubmitted).\
            grid(row = 1, column = 6, sticky = W + E)
        labelTextList = ["Cusine", "Restaurant name", "Address", "Inspection Score"]
        columnList = [1, 2, 3, 4]
        for i in columnList:
            Label(window, text = labelTextList[i-1]).grid(row = 2, column = i, sticky = W + E)

    def buildViewRestaurantsWithComplaintsWindow(self, window):
        # Back Button
        Button(window, text = "Back",
               command = self.backFromViewRestaurantsWithComplaintsWindowToInspectorCriteriaWindow).\
            grid(row = 1, column = 1, sticky = E)

        # Year Label
        Label(window, text = "Enter Year: yyyy").grid(row = 1, column = 2, sticky = W + E)

        # Year Entry
        self.year_restaurantsWithComplaints = StringVar()
        Entry(window, textvariable = self.year_restaurantsWithComplaints, width = 30).\
            grid(row = 1, column = 3, sticky = W + E)

        # Min Number of Complaints Label
        Label(window, text = "Enter Min Complaints").grid(row = 1, column = 4, sticky = W + E)
        # Number of Complaints >= Entry
        self.minComplaints = StringVar()
        Entry(window, textvariable = self.minComplaints, width = 30).grid(row = 1, column = 5, sticky = W + E)

        # Max Score Label
        Label(window, text = "Enter Max Score").grid(row = 1, column = 6, sticky = W + E)

        # Max Score Entry
        self.maxScore = StringVar()
        Entry(window, textvariable = self.maxScore, width = 30).grid(row = 1, column = 7, sticky = W + E)

        # View Button
        Button(window, text = "View",
               command = self.viewRestaurantsWithComplaintsButtonClicked_infoSubmitted).\
            grid(row = 1, column = 8, sticky = W + E)

#-------------------BUILD INSERT REPORT WINDOW METHOD------------------------------------------

    def buildInsertReportWindow(self, window):
        # Inspector ID Label
        inspectorIDLabel = Label(window, text = "Inspector ID")
        inspectorIDLabel.grid(row = 1, column = 1, sticky = W + E)

        # Inspector ID Entry
        self.inspectorID = StringVar()
        inspectorIDEntry = Entry(window, textvariable = self.inspectorID, width = 30)
        inspectorIDEntry.grid(row = 1, column = 2, sticky = W + E)

        # Restaurant ID Label
        restaurantIDLabel = Label(window, text = "Restaurant ID")
        restaurantIDLabel.grid(row = 1, column = 3, sticky = W + E)

        # Restaurant ID Entry
        self.restaurantID = StringVar()
        restaurantIDEntry = Entry(window, textvariable = self.restaurantID, width = 30)
        restaurantIDEntry.grid(row = 1, column = 4, sticky = W + E)

        # Date Label
        dateLabel = Label(window, text = "Date, yyyy-mm-dd")
        dateLabel.grid(row = 1, column = 5, sticky = W + E)

        # Date Entry
        self.date = StringVar()
        dateEntry = Entry(window, textvariable = self.date, width = 30)
        dateEntry.grid(row = 1, column = 6, sticky = W + E)

        # Item Number Label
        itemNumberLabel = Label(window, text = "Item Number")
        itemNumberLabel.grid(row = 2, column = 1, sticky = W + E)

        # Item Description Label
        itemDescriptionLabel = Label(window, text = "Item Description")
        itemDescriptionLabel.grid(row = 2, column = 2, columnspan = 3, sticky = W + E)

        # Critical Label
        criticalLabel = Label(window, text = "Critical")
        criticalLabel.grid(row = 2, column = 5, sticky = W + E)

        # Score Label
        scoreLabel = Label(window, text = "Score")
        scoreLabel.grid(row = 2, column = 6, sticky = W + E)

        # Comment Label
        commentLabel = Label(window, text = "Comment(optional)", width = 40)
        commentLabel.grid(row = 2, column = 7, sticky = W + E)

        # Grid all the item numbers
        # We will have a list if item numbers retrieved form the database.
        # To test my GUI, they are hard-coded temporarily.
        self.cursor.execute("SELECT * FROM item")
        itemTuple = self.cursor.fetchall()
        itemNumberList = []
        itemDescriptionList = []
        itemCriticalList = []
        for i in itemTuple:
            itemNumberList.append(i[0])
            itemDescriptionList.append(str(i[2]))
            itemCriticalList.append(str(i[3]))
        for i in itemNumberList:
            Label(window, text = i).grid(row = 2 + i, column = 1, sticky = W)

        # Grid all the item descriptions
        for i in range(0, len(itemDescriptionList)):
            Label(window, text = itemDescriptionList[i]).grid(row = 3 + i,
                                                                          column = 2, columnspan = 3, sticky = W)

        # Grid all the item criticals
        for i in range(0, len(itemCriticalList)):
            Label(window, text = itemCriticalList[i]).grid(row = 3 + i, column = 5, sticky = W)

        # Create 15 score entries
        self.itemScoreList = []
        self.itemScoreEntryList = []
        for i in range(0, 15):
            (aScore, anEntry) = self.createAnEntry(3 + i, 6, 30, window)
            self.itemScoreList.append(aScore)
            self.itemScoreEntryList.append(anEntry)

        # Create 15 Comment Entries
        self.commentList = []
        self.commentEntryList = []
        for i in range(0,15):
            (aComment, aCommentEntry) = self.createAnEntry(3 + i, 7, 40, window)
            self.commentList.append(aComment)
            self.commentEntryList.append(aCommentEntry)

        # Submit Button
        submitButton = Button(window, text = "Submit", command = self.submitReportButtonClicked)
        submitButton.grid(row = 18, column = 7, sticky = W + E)

        # Back Button
        backButton = Button(window, text = "Back", command = self.backFromInsertReportToInspectorMenu)
        backButton.grid(row = 18, column = 6, sticky = W + E)

#--------------SUBMIT REPORT METHOD----------------------------------------

    def submitReportButtonClicked(self):
        for i in range(0, 15):
            if not self.itemScoreList[i].get():
                messagebox.showwarning("Empty input", "Please enter a score for each item.")
                return False
        for i in range(0, 8):
            if not (int(self.itemScoreList[i].get()) in range(0, 10)):
                messagebox.showwarning("Input out of range", "For items 1-8, the score must be 0-9. You entered "
                                       + self.itemScoreList[i].get() + " for item " + str(i + 1) + ".")
                return False
        for i in range(8, 15):
            if not (int(self.itemScoreList[i].get()) in range(0, 5)):
                messagebox.showwarning("Input out of range", "For items 9-15, the score must be 0-4. You entered "
                                       + self.itemScoreList[i].get() + " for item " + str(i + 1) + ".")
                return False
        result = self.cursor.execute("SELECT iid FROM inspector WHERE iid = %s", self.inspectorID.get())
        if not result:
            messagebox.showwarning("Inspector ID is not exist")
            return False
        result = self.cursor.execute("SELECT rid FROM restaurant WHERE rid = %s", self.restaurantID.get())
        if not result:
            messagebox.showwarning("Restaurant ID is not exist")
            return False
        self.submitReportToDatabase()
        messagebox.showwarning("Submission successful", "Your report has been submitted.")
        self.insertReportWindow.withdraw()
        self.inspectorMenuWindow.deiconify()
        return True
#----------DATABASE INTERACTION METHODS---------------------------------------------
    def submitReportToDatabase(self):
        totalscore = 0
        passfail = 'PASS'
        for i in range(len(self.itemScoreList)):
            if i + 1 <= 8:
                if int(self.itemScoreList[i].get()) < 8:
                    passfail = 'FAIL'
            totalscore = totalscore + int(self.itemScoreList[i].get())
        if totalscore < 75:
            passfail = 'FAIL'
        insertInfoQuery = 'INSERT INTO inspection (rid, iid, idate, totalscore, passfail) VALUES (%s, %s, %s, %s, %s)'
        self.cursor.execute(insertInfoQuery,
                            (self.restaurantID.get(), self.inspectorID.get(), self.date.get(), totalscore, passfail))
        self.db.commit()
        insertInfoQuery = 'INSERT INTO contains (itemnum, rid, idate, score) VALUES(%s, %s, %s, %s)'
        for i in range(len(self.itemScoreList)):
            self.cursor.execute(insertInfoQuery, (i + 1, self.restaurantID.get(), self.date.get(), self.itemScoreList[i].get()))
            self.db.commit()
        insertInfoQuery = 'INSERT INTO includes (itemnum, rid, idate, comment) VALUES(%s, %s, %s, %s)'
        for i in range(len(self.commentList)):
            if self.commentList[i].get():
                self.cursor.execute(insertInfoQuery, (i+1, self.restaurantID.get(),self.date.get(),self.commentList[i].get()))
                self.db.commit()
#----------BACK METHODS------------------------------------------------------------------------------------

    def backFromInsertReportToInspectorMenu(self):
        self.insertReportWindow.withdraw()
        self.inspectorMenuWindow.deiconify()

    def backFromViewReportsByMonthAndYearWindowToInspectorMenu(self):
        self.viewReportsByMonthAndYearWindow.withdraw()
        self.inspectorMenuWindow.deiconify()

    def backFromViewReportsByMonthAndYearForACountyWindowToInspectorMenu(self):
        self.viewReportsByMonthAndYearForACountyWindow.withdraw()
        self.inspectorMenuWindow.deiconify()

    def backFromViewtopRestaurantByCuisineForAYearAndCountyWindowToInspectorMenuWindow(self):
        self.viewTopRestaurantByCuisineForAYearAndCountyWindow.withdraw()
        self.inspectorMenuWindow.deiconify()

    def backFromViewRestaurantsWithComplaintsWindowToInspectorCriteriaWindow(self):
        self.viewRestaurantsWithComplaintsWindow.withdraw()
        self.inspectorMenuWindow.deiconify()

    def backFromViewReportsCriteriaWindow(self):
        self.viewReportsCriteriaWindow.withdraw()
        self.inspectorMenuWindow.deiconify()

#---------VIEW BUTTON CLICKED_INFO SUBMITTED METHODS----------------------------------------------------
    def viewReportsByMonthAndYearButtonClicked_infoSubmitted(self):
        try:
            self.displayReportsByMonthAndYear(self.monthOfReportByMonthAndYear.get(),
                                          self.yearOfReportByMonthAndYear.get(),
                                          self.viewReportsByMonthAndYearWindow, self.gridList1)
        except:
            self.displayReportsByMonthAndYear(self.monthOfReportByMonthAndYear.get(),
                                          self.yearOfReportByMonthAndYear.get(),
                                          self.viewReportsByMonthAndYearWindow, [])

    def viewReportsByMonthAndYearForACountyButtonClicked_infoSubmitted(self):
        try:
            self.displayReportsByMonthAndYearForACounty(self.yearOfReportByYearAndCounty.get(),
                                                    self.countyInspectedByYearAndCounty.get(),
                                                    self.viewReportsByMonthAndYearForACountyWindow, self.gridList2)
        except:
            self.displayReportsByMonthAndYearForACounty(self.yearOfReportByYearAndCounty.get(),
                                                    self.countyInspectedByYearAndCounty.get(),
                                                    self.viewReportsByMonthAndYearForACountyWindow, [])

    def viewTopRestaurantByCuisineForAYearAndCountyButtonClicked_infoSubmitted(self):
        try:
            self.displayTopRestaurantByCuisineForAYearAndCounty(self.yearOfReport_topRestaurant.get(),
                                                            self.countyInspected_topRestaurant.get(),
                                                            self.viewTopRestaurantByCuisineForAYearAndCountyWindow,
                                                                self.gridList3)
        except:
            self.displayTopRestaurantByCuisineForAYearAndCounty(self.yearOfReport_topRestaurant.get(),
                                                            self.countyInspected_topRestaurant.get(),
                                                            self.viewTopRestaurantByCuisineForAYearAndCountyWindow, [])

    def viewRestaurantsWithComplaintsButtonClicked_infoSubmitted(self):
        try:
            self.displayRestaurantsWithComplaints(self.minComplaints.get(),
                                              self.maxScore.get(),
                                              self.viewRestaurantsWithComplaintsWindow, self.gridList4)
        except:
            self.displayRestaurantsWithComplaints(self.minComplaints.get(),
                                              self.maxScore.get(),
                                              self.viewRestaurantsWithComplaintsWindow, [])

#--------------------DISPLAY SUMMARY INFO BY CRITERIA METHODS------------------------
    def displayReportsByMonthAndYear(self, month, year, window, gridList):
        # Clear window
        for i in range(len(gridList)):
            for j in range(len(gridList[i])):
                Label(window, text = gridList[i][j]).grid(row = 3 + j, column = 1 + i, sticky = W + E)

        viewInfoQuery = 'CREATE VIEW MonthlyReport (County, Cuisine,numInspected,numFailed) AS SELECT county, cuisine, COUNT(*), SUM(IF(passfail ="FAIL", 1,0)) FROM inspection NATURAL JOIN restaurant WHERE STRCMP(substring(idate, 6, 2), %s) = 0 AND STRCMP(substring(idate, 1, 4), %s) = 0 GROUP BY County,Cuisine'
        result = self.cursor.execute(viewInfoQuery, (month, year))
        self.countyList = []
        self.cuisineList = []
        self.numberOfRestaurantsInspectedList = []
        self.NumberOfFailedList = []
        self.cursor.execute('SELECT County FROM MonthlyReport')
        reportCountyTuple = self.cursor.fetchall()
        for i in reportCountyTuple:
            self.countyList.append(i)
        for i in range(0, len(self.countyList)):
            Label(window, text = self.countyList[i]).\
                grid(row = 3 + i, column = 1, sticky = W + E)
        self.cursor.execute('SELECT Cuisine FROM MonthlyReport')
        reportCuisineTuple = self.cursor.fetchall()
        for i in reportCuisineTuple:
            self.cuisineList.append(i)
        for i in range(0, len(self.cuisineList)):
            Label(window, text = self.cuisineList[i]).\
                grid(row = 3 + i, column = 2, sticky = W + E)
        self.cursor.execute('SELECT numInspected FROM MonthlyReport')
        reportInspectedTuple = self.cursor.fetchall()
        for i in reportInspectedTuple:
            self.numberOfRestaurantsInspectedList.append(i[0])
        for i in range(0, len(self.numberOfRestaurantsInspectedList)):
            Label(window, text = self.numberOfRestaurantsInspectedList[i]).\
                grid(row = 3 + i, column = 3, sticky = W + E)
        self.cursor.execute('SELECT numFailed FROM MonthlyReport')
        reportFailedTuple = self.cursor.fetchall()
        for i in reportFailedTuple:
            self.NumberOfFailedList.append(i[0])
        for i in range(0, len(self.NumberOfFailedList)):
            Label(window, text = self.NumberOfFailedList[i]).\
                grid(row = 3 + i, column = 4, sticky = W + E)
        dropQuery = 'DROP VIEW MonthlyReport'
        self.cursor.execute(dropQuery)

        self.gridList1 = [self.countyList, self.cuisineList, self.numberOfRestaurantsInspectedList, self.NumberOfFailedList]
        for i in range(len(self.gridList1)):
            for j in range(len(self.gridList1[i])):
                self.gridList1[i][j] = '         '

    def displayReportsByMonthAndYearForACounty(self, year, county, window, gridList2):
        # Clear Window
        for i in range(len(gridList2)):
            Label().grid(row = 2 + i, column = 2, sticky = W + E)

        # Month Labels
        monthLabelList = ["Month", "January", "February","March", "April", "May", "June", "July",
                          "August", "September", "October", "November", "December", "Grand Total"]
        for i in range(0, 14):
            Label(window, text = monthLabelList[i]).grid(row = 2 + i, column = 1, sticky = W + E)

        # Number of Restaurants Inspected, by Month
        # This list is hardcoded temporarily
        numberOfRestaurantsInspectedList = ["Restaurants Inspected"]
        for i in range(1,13):
            if (i < 10):
                month = '0' + str(i)
            else:
                month = str(i)
            self.cursor.execute("SELECT COUNT(*) FROM inspection NATURAL JOIN restaurant WHERE STRCMP(substring(idate,1,4),%s) = 0 AND STRCMP(substring(idate,6,2),%s)= 0 AND county = %s", (year, month, county))
            result = self.cursor.fetchall()
            for i in result:
                numberOfRestaurantsInspectedList.append(str(result[0][0]))
        total = 0
        for i in range(1,len(numberOfRestaurantsInspectedList)):
            total = total + int(numberOfRestaurantsInspectedList[i])
        numberOfRestaurantsInspectedList.append(total)
        for i in range(0, 14):
            Label(window, text = numberOfRestaurantsInspectedList[i]).\
                grid(row = 2 + i, column = 2, sticky = W + E)
        # Clear List
        self.gridList2 = numberOfRestaurantsInspectedList
        for i in range(len(self.gridList2)):
            self.gridList2[i] = '         '

    def displayTopRestaurantByCuisineForAYearAndCounty(self, year, county, window, gridList3):
        # Clear Window
        for i in range(len(gridList3)):
            for j in range(len(gridList3[i])):
                Label(window, text = gridList3[i][j]).grid(row = 3 + j, column = 1 + i, sticky = W + E)

        # Cuisine
        self.cursor.execute('CREATE VIEW INSPECTION_ORDER_BY_SCORE AS SELECT * FROM inspection ORDER BY totalscore DESC')
        infoQuery = 'CREATE VIEW CUISINE_WITH_RESTAURANT(restaurantID, restaurantName, address, cuisine, totalscore) AS SELECT DISTINCT r.rid, name, CONCAT(street," ", city, " ", state," ", zipcode), cuisine, totalscore FROM restaurant AS r NATURAL JOIN INSPECTION_ORDER_BY_SCORE WHERE county = %s AND STRCMP(substring(idate, 1, 4), %s) = 0 ORDER BY cuisine'
        self.cursor.execute(infoQuery, (county, year))
        self.cuisineList = []
        self.restaurantNameList = []
        self.addressList = []
        self.ScoreList = []
        self.cursor.execute('SELECT cuisine FROM CUISINE_WITH_RESTAURANT AS c WHERE NOT EXISTS (SELECT r.totalscore FROM CUISINE_WITH_RESTAURANT AS r WHERE c.cuisine = r.cuisine AND c.totalscore < r.totalscore)')
        reportCuisineTuple = self.cursor.fetchall()
        for i in reportCuisineTuple:
            self.cuisineList.append(i)
        for i in range(0, len(self.cuisineList)):
            Label(window, text = self.cuisineList[i]).\
                grid(row = 3 + i, column = 1, sticky = W + E)
        self.cursor.execute('SELECT restaurantName FROM CUISINE_WITH_RESTAURANT AS c WHERE NOT EXISTS (SELECT r.totalscore FROM CUISINE_WITH_RESTAURANT AS r WHERE c.cuisine = r.cuisine AND c.totalscore < r.totalscore)')
        reportRestaurantTuple = self.cursor.fetchall()
        for i in reportRestaurantTuple:
            self.restaurantNameList.append(str(i))
        for i in range(0, len(self.restaurantNameList)):
            Label(window, text = self.restaurantNameList[i].split("\'")[1]).\
                grid(row = 3 + i, column = 2, sticky = W + E)
        self.cursor.execute('SELECT address FROM CUISINE_WITH_RESTAURANT AS c WHERE NOT EXISTS (SELECT r.totalscore FROM CUISINE_WITH_RESTAURANT AS r WHERE c.cuisine = r.cuisine AND c.totalscore < r.totalscore)')
        reportAddressTuple = self.cursor.fetchall()
        for i in reportAddressTuple:
            self.addressList.append(i[0])
        for i in range(len(self.addressList)):
            address = self.addressList[i]
            Label(window, text = address).\
                grid(row = 3 + i, column = 3, sticky = W + E)
        self.cursor.execute('SELECT totalscore FROM CUISINE_WITH_RESTAURANT AS c WHERE NOT EXISTS (SELECT r.totalscore FROM CUISINE_WITH_RESTAURANT AS r WHERE c.cuisine = r.cuisine AND c.totalscore < r.totalscore)')
        reportScoreTuple = self.cursor.fetchall()
        for i in reportScoreTuple:
            self.ScoreList.append(i)
        for i in range(0, len(self.ScoreList)):
            Label(window, text = self.ScoreList[i]).\
                grid(row = 3 + i, column = 4, sticky = W + E)
        self.cursor.execute('DROP VIEW INSPECTION_ORDER_BY_SCORE')
        self.cursor.execute('DROP VIEW CUISINE_WITH_RESTAURANT')

        self.gridList3 = [self.cuisineList, self.restaurantNameList, self.addressList, self.ScoreList]
        for i in range(len(self.gridList3)):
            for j in range(len(self.gridList3[i])):
                self.gridList3[i][j] = "       "

    def displayRestaurantsWithComplaints(self, minComplaints, maxScore, window, gridList4):
        # Clear Window
        for i in range(len(gridList4)):
            for j in range(len(gridList4[i])):
                Label(window, text = gridList4[i][j]).grid(row = 3 + j, column = 1 + i, sticky = W + E)
        
        
        
        
        self.cursor.execute('CREATE VIEW REPORT_OF_COMPLAINTS (restaurantName, restaurantID, numberOfComplaint, description) AS SELECT name, c.rid, COUNT(*), description FROM complaint AS c LEFT OUTER JOIN restaurant AS r ON c.rid = r.rid GROUP BY c.rid HAVING COUNT(*) >= %s', (minComplaints))
        self.cursor.execute('CREATE VIEW REPORT_OF_SCORE (restaurantName, address, operatorEmail, totalScore, idate) AS SELECT name, CONCAT(county, street, city, " ", state, " ", zipcode), email, totalscore, idate FROM restaurant NATURAL JOIN inspection AS n WHERE NOT EXISTS(SELECT n.idate FROM inspection AS i WHERE i.idate > n.idate AND n.rid = i.rid) HAVING totalscore < %s', maxScore)
        self.cursor.execute('CREATE VIEW NEW(name, rrid, address, operatorEmail, numberOfComplaint, description, totalscore, idate) AS SELECT r.restaurantName, restaurantID, address, operatorEmail, numberOfComplaint, description, totalscore, idate FROM REPORT_OF_COMPLAINTS AS r LEFT OUTER JOIN REPORT_OF_SCORE AS s ON r.restaurantName = s.restaurantName')
        self.cursor.execute('CREATE VIEW OPERATORNAME(name, rrid, address, operatorEmail, operatorName, numberOfComplaint, description, totalscore, idate) AS SELECT name, rrid, address, operatorEmail, CONCAT(firstname, " ", lastname), numberOfComplaint, description, totalscore, idate FROM NEW AS n NATURAL JOIN operatorowner AS o WHERE n.operatorEmail = o.email')
        self.cursor.execute('CREATE VIEW ReportByComplaintsNumberScore(RestaurantName, address, operatorEmail, operatorName, numberOfComplaint, description, totalscore, idate) AS SELECT name, address, operatorEmail, operatorName, numberOfComplaint, complaint.description, totalscore, idate FROM OPERATORNAME LEFT OUTER JOIN complaint ON rrid = rid')
        itemTuple = self.cursor.fetchall()
        self.restaurantNameList = ["Restaurant name"]
        self.addressList = ["Address"]
        self.operatorEmailList = ["Email"]
        self.scoreList = ["score"]
        self.descriptionList = ["description"]
        self.operatorNameList = ["Operator"]
        self.numberList = ["number Of Complaint"]
        self.numberOfComplaintsList = []

        self.cursor.execute('SELECT numberOfComplaint FROM ReportByComplaintsNumberScore as r WHERE EXISTS (SELECT * FROM contains AS q WHERE r.idate = q.idate AND q.score < 9)GROUP BY RestaurantName')
        reportTuple = self.cursor.fetchall()   
        for i in reportTuple:
            self.numberOfComplaintsList.append(i)


        self.cursor.execute('SELECT DISTINCT RestaurantName FROM ReportByComplaintsNumberScore as r WHERE EXISTS (SELECT * FROM contains AS q WHERE r.idate = q.idate AND q.score < 9)')
        reportTuple = self.cursor.fetchall()   
        for i in range(len(reportTuple)):
            self.restaurantNameList.append(reportTuple[i][0])
            for j in range(1, self.numberOfComplaintsList[i][0]):
                self.restaurantNameList.append("")

        self.cursor.execute('SELECT numberOfComplaint FROM ReportByComplaintsNumberScore as r WHERE EXISTS (SELECT * FROM contains AS q WHERE r.idate = q.idate AND q.score < 9) GROUP BY RestaurantName ')
        reportTuple = self.cursor.fetchall()   
        for i in range(len(reportTuple)):
            self.numberList.append(reportTuple[i][0])
            for j in range(1, self.numberOfComplaintsList[i][0]):
                self.numberList.append("")

        self.cursor.execute('SELECT DISTINCT address FROM ReportByComplaintsNumberScore as r WHERE EXISTS (SELECT * FROM contains AS q WHERE r.idate = q.idate AND q.score < 9)')
        reportTuple = self.cursor.fetchall()   
        for i in range(len(reportTuple)):
            self.addressList.append(reportTuple[i][0])
            for j in range(1, self.numberOfComplaintsList[i][0]):
                self.addressList.append("")


        self.cursor.execute('SELECT operatorEmail FROM ReportByComplaintsNumberScore as r WHERE EXISTS (SELECT * FROM contains AS q WHERE r.idate = q.idate AND q.score < 9) GROUP BY RestaurantName ')
        reportTuple = self.cursor.fetchall()
        for i in range(len(reportTuple)):
            self.operatorEmailList.append(reportTuple[i][0])
            for j in range(1, self.numberOfComplaintsList[i][0]):
                self.operatorEmailList.append("")


        self.cursor.execute('SELECT operatorName FROM ReportByComplaintsNumberScore as r WHERE EXISTS (SELECT * FROM contains AS q WHERE r.idate = q.idate AND q.score < 9)GROUP BY RestaurantName ')
        reportTuple = self.cursor.fetchall()
        for i in range(len(reportTuple)):
            self.operatorNameList.append(reportTuple[i][0])    
            for j in range(1, self.numberOfComplaintsList[i][0]):
                self.operatorNameList.append("")


        self.cursor.execute('SELECT DISTINCT description FROM ReportByComplaintsNumberScore as r WHERE EXISTS (SELECT * FROM contains AS q WHERE r.idate = q.idate AND q.score < 9)')
        reportTuple = self.cursor.fetchall()   
        for i in range(len(reportTuple)):
            self.descriptionList.append(reportTuple[i][0])

        self.cursor.execute('SELECT DISTINCT totalscore FROM ReportByComplaintsNumberScore AS c WHERE NOT EXISTS (SELECT r.totalscore FROM ReportByComplaintsNumberScore AS r WHERE c.restaurantName = r.restaurantName AND c.idate < r.idate) AND EXISTS (SELECT * FROM contains AS q WHERE c.idate = q.idate AND q.score < 9)')
        reportTuple = self.cursor.fetchall()
        for i in range(len(reportTuple)):
            self.scoreList.append(reportTuple[i][0])
            for j in range(1, self.numberOfComplaintsList[i][0]):
                self.scoreList.append("")

        for i in range(0, len(self.addressList)):
            Label(window, text = self.restaurantNameList[i]).\
                grid(row = 3 + i, column = 1, sticky = W + E)
            Label(window, text = self.addressList[i]).\
                grid(row = 3 + i, column = 2, sticky = W + E)
            Label(window, text = self.operatorNameList[i]).\
                grid(row = 3 + i, column = 3, sticky = W + E)
            Label(window, text = self.operatorEmailList[i]).\
                grid(row = 3 + i, column = 4, sticky = W + E)
            Label(window, text = self.scoreList[i]).\
                grid(row = 3 + i, column = 5, sticky = W + E)
            Label(window, text = self.descriptionList[i]).\
                grid(row = 3 + i, column = 6, sticky = W + E)
            Label(window, text = self.numberList[i]).\
                grid(row = 3 + i, column = 7, sticky = W + E)
        self.cursor.execute('DROP VIEW REPORT_OF_SCORE')
        self.cursor.execute('DROP VIEW NEW')
        self.cursor.execute('DROP VIEW REPORT_OF_COMPLAINTS')
        self.cursor.execute('DROP VIEW OPERATORNAME')
        self.cursor.execute('DROP VIEW ReportByComplaintsNumberScore')
        
        self.gridList4 = [self.restaurantNameList, self.addressList, self.operatorNameList, self.operatorEmailList, self.scoreList, self.descriptionList, self.numberList]
        for i in range(len(self.gridList4)):
            for j in range(len(self.gridList4[i])):
                self.gridList4[i][j] = "       "
        
        
#-----------------------HELPER METHODS----------------------------

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