import tkinter as tk
import tkinter.font as tkFont
import webbrowser

import mysql.connector

bgColor = "#990000"
fgColor = "white"
root = tk.Tk()


def changeUser(user):
    global currUser
    currUser = user


mydb = mysql.connector.connect(host="localhost", username="root", password="", database="hackathon")
mycursor = mydb.cursor()


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()

        # Create canvas
        canvas = tk.Canvas(root, height=500, width=800)
        canvas.pack()

        self.currFrame = None
        self.switchScene(startScene)

    def switchScene(self, newFrame):
        if self.currFrame is not None:
            for widget in self.currFrame.winfo_children():
                widget.destroy()
            self.currFrame.forget()
            self.currFrame.destroy()

        self.currFrame = newFrame(self)
        self.currFrame.pack()


    def displayDetails(self, charity):
        newWindow = tk.Toplevel(bg=bgColor)
        try:
            tk.Label(newWindow, text="", bg=bgColor).pack(side="top")

            # name
            tk.Message(newWindow, text=charity[0], bg=bgColor, fg=fgColor, width=900, font=tkFont.Font(size=20)).pack(side="top")

            # motto
            tk.Message(newWindow, text=charity[1], bg=bgColor, fg=fgColor, width=900, font=tkFont.Font(size=12), justify=tk.LEFT).pack(side="top")
            tk.Label(newWindow, text="", font=tkFont.Font(size=6), bg=bgColor, fg=fgColor).pack(side="top")

            # description
            tk.Message(newWindow, text="Description: " + charity[2], bg=bgColor, fg=fgColor, width=800, font=tkFont.Font(size=12), justify=tk.LEFT).pack(side="top")

            # score
            tk.Message(newWindow, text="Score: " + str(round(charity[3]/10, 1)) + " / 10", bg=bgColor, fg=fgColor, width=900, font=tkFont.Font(size=12), justify=tk.LEFT).pack(side="top")

            # category
            tk.Message(newWindow, text="Categories : " + charity[4], bg=bgColor, fg=fgColor, width=900, font=tkFont.Font(size=12), justify=tk.LEFT).pack(side="top")

            # subcategory
            tk.Message(newWindow, text="Subcategories: " + charity[5], bg=bgColor, fg=fgColor, width=900, font=tkFont.Font(size=12), justify=tk.LEFT).pack(side="top")

            # Website
            if len(charity[6]) > 1:
                website = tk.Message(newWindow, text="Website", bg=bgColor, fg="blue", cursor="hand2", justify=tk.LEFT).pack(side="top")
                website.bind("<Button-1>", lambda e: webbrowser.open_new(charity[6]))

            # Facebook
            if len(charity[7]) > 1:
                facebook = tk.Message(newWindow, text="Facebook", bg=bgColor, fg="blue", cursor="hand2", justify=tk.LEFT).pack(side="top")
                facebook.bind("<Button-1>", lambda e: webbrowser.open_new(charity[7]))

            # Twitter
            if len(charity[8]) > 1:
                twitter = tk.Message(newWindow, text="Twitter", bg=bgColor, fg="blue", cursor="hand2", justify=tk.LEFT).pack(side="top")
                twitter.bind("<Button-1>", lambda e: webbrowser.open_new(charity[8]))

            # Address | City
            tk.Message(newWindow, text="Location: " + charity[9] + ", " + charity[10] + ", " + charity[11], bg=bgColor, fg=fgColor, width=900, font=tkFont.Font(size=12), justify=tk.LEFT).pack(side="top")

            # Bottom Spacing
            tk.Label(newWindow, text="", bg=bgColor, fg=fgColor, font=tkFont.Font(size=20)).pack(side="bottom")

            # Donate
            tk.Button(newWindow, text="Donate", width=60, height=3).pack(side="bottom")

            # Bottom Spacing
            tk.Label(newWindow, text="", bg=bgColor, fg=fgColor, font=tkFont.Font(size=20)).pack(side="bottom")

            # Favorite
            tk.Button(newWindow, text="Favorite", width=60, height=3).pack(side="bottom")

            # Bottom Spacing
            tk.Label(newWindow, text="", bg=bgColor, fg=fgColor, font=tkFont.Font(size=20)).pack(side="bottom")


        except:
            pass

    def createBackButton(self, frame, scene):
        backButton = tk.Button(frame, text="Back", command=lambda: self.switchScene(scene))
        backButton.place(relx=.01, rely=0.025, relw=.2, relh=.1)


# Home Scene - Nothing atm
class homeScene(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Container
        frame = tk.Frame(root, bg=bgColor)
        frame.place(relx=.2, relwidth=.8, relheight=1)

        # Side Bar Container
        sideBar = tk.Canvas(root, bg="#660000")
        sideBar.place(relx=0, relh=1, relw=.2)

        # Button 1 - Matches
        resultsButton = tk.Button(sideBar, text="My Matches", command=lambda: self.master.switchScene(resultScene))
        resultsButton.place(relx=.1, rely=0.025, relw=.8, relh=.1)

        # Button 2 - Profile
        profileButton = tk.Button(sideBar, text="Profile", command=lambda: self.master.switchScene(accountScene))
        profileButton.place(relx=.1, rely=0.15, relw=.8, relh=.1)

        # Button 4 - Log Out
        logOutButton = tk.Button(sideBar, text="Log Out", command=lambda: self.master.switchScene(checkScene))
        logOutButton.place(relx=.1, rely=0.875, relw=.8, relh=.1)

        # Fill Categories
        sql ="SELECT category, COUNT(*) as count from charnavandusachar GROUP BY category HAVING COUNT(*) > 100 ORDER BY count DESC"
        mycursor.execute(sql)
        result = mycursor.fetchall()

        listOfCategories = []
        for category in result:
            listOfCategories.append(category[0])

        # Drop
        selected = tk.StringVar()
        selected.set("Select a Category")
        categories = tk.OptionMenu(frame, selected, *listOfCategories)
        categories.place(relx=.675, rely=.15, relw=.3, relh=.05)


        # Factors/Characteristics

        # Small Charities
        fac1 = tk.BooleanVar()
        fac1.set(False)
        box1 = tk.Checkbutton(frame, text="Small Charities", bg=bgColor, fg=fgColor, selectcolor="black", variable=fac1)
        box1.place(relx=.675, rely=.225, relw=.3, relh=.05)

        # High Transparency Charities
        fac2 = tk.BooleanVar()
        fac2.set(False)
        box2 = tk.Checkbutton(frame, text="High Transparency Charities", bg=bgColor, fg=fgColor, selectcolor="black", variable=fac2)
        box2.place(relx=.675, rely=.275, relw=.3, relh=.05)

        # Low Financial Health Charities
        fac3 = tk.BooleanVar()
        fac3.set(False)
        box3 = tk.Checkbutton(frame, text="Low Financial Health Charities", bg=bgColor, fg=fgColor, selectcolor="black",
                              variable=fac3)
        box3.place(relx=.675, rely=.35, relw=.3, relh=.05)

        # High Rated Charities
        fac4 = tk.BooleanVar()
        fac4.set(False)
        box4 = tk.Checkbutton(frame, text="High Rated Charities", bg=bgColor, fg=fgColor, selectcolor="black",
                              variable=fac4)
        box4.place(relx=.675, rely=.425, relw=.3, relh=.05)

        # Highly Expense Charities
        fac5 = tk.BooleanVar()
        fac5.set(False)
        box5 = tk.Checkbutton(frame, text="Highly Expense Charities", bg=bgColor, fg=fgColor, selectcolor="black",
                              variable=fac5)
        box5.place(relx=.675, rely=.5, relw=.3, relh=.05)

        # Results
        tk.Message(frame, text="Search for a Charity", width=900, bg=bgColor, fg=fgColor, font=tkFont.Font(size="20")).pack(side="top")
        tk.Label(frame, text="Select as many categories as you would like", bg=bgColor, fg=fgColor).pack(side="top")

        def searching():
            results = tk.Listbox(frame)
            scrollBar = tk.Scrollbar(results)

            # Query Results
            whereClause = ""

            #Count how many factors we have
            factorCount = 0
            if fac1.get() == True:
                factorCount+=1

            if fac2.get() == True:
                factorCount+=1

            if fac3.get() == True:
                factorCount+=1

            if fac4.get() == True:
                factorCount+=1

            if fac5.get() == True:
                factorCount+=1

            # If we have 1 or more factors selected
            if factorCount > 0:
                whereClause += " AND"

            # Small Charities
            if fac1.get() == True:
                whereClause += " size = 'small'"
                factorCount -= 1
                if factorCount > 0:
                    whereClause += " AND "


            # High Transparency Charities
            if fac2.get() == True:
                whereClause += " ascore > 50"
                factorCount -= 1
                if factorCount > 0:
                    whereClause += " AND "

            # Low Financial Health Charities
            if fac3.get() == True:
                whereClause += " fscore < 50"
                factorCount -= 1
                if factorCount > 0:
                    whereClause += " AND "

            # High Rated Charities
            if fac4.get() == True:
                whereClause += " score > 50"
                factorCount -= 1
                if factorCount > 0:
                    whereClause += " AND "

            # Highly Expense Charities
            if fac5.get() == True:
                whereClause += " tot_exp > 50"

            sql = "SELECT name, motto, description, score, category, subcategory, Website, Facebook, Twitter, Address, city, state FROM charnavandusachar WHERE category = " + "'" + selected.get() + "'" + whereClause
            mycursor.execute(sql)
            result2 = mycursor.fetchall()

            for x in result2:
                results.insert(tk.END, x[0])

            results.place(relx=.05, rely=.15, relw=.6, relh=.8)
            results.config(yscrollcommand=scrollBar.set)
            scrollBar.pack(side="right", fill="y")
            scrollBar.config(command=results.yview)

            # Details Button
            details = tk.Button(frame, text="Details",
                                command=lambda: self.master.displayDetails(result2[results.curselection()[0]]))
            details.place(relx=.75, rely=.925, relw=.15, relh=.05)

        # Search Button
        search = tk.Button(frame, text="Search", command=lambda: searching())
        search.place(relx=.75, rely=.85, relw=.15, relh=.05)


# Starting Page - Click to begin
class startScene(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Creates Frame to place objects
        frame = tk.Frame(root, bg=bgColor)
        frame.place(relwidth=1, relheight=1)

        # Top Buffer
        tk.Label(frame, text="", bg=bgColor, font=tkFont.Font(size=30)).pack(side="top")

        # Top Message
        header = tk.Message(frame, text="Welcome to the Charity Matchmaker!", bg=bgColor, fg=fgColor,
                            font=tkFont.Font(size=30), justify="center", width=400)
        header.pack(side="top")

        # Bottom Buffer
        tk.Label(frame, text="", bg=bgColor, font=tkFont.Font(size=60)).pack(side="bottom")

        # Begin Button
        beginButton = tk.Button(frame, text="Click here to Begin", bg="white", fg="black", font=tkFont.Font(size=20),
                                width=40, command=lambda: self.master.switchScene(checkScene))
        beginButton.pack(side="bottom")


# Login or Register Scene
class checkScene(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        frame = tk.Frame(root, bg=bgColor)
        frame.place(relwidth=1, relheight=1)

        changeUser(-1)

        login = tk.Button(frame, text="Login", font=tkFont.Font(size=20),
                          command=lambda: self.master.switchScene(loginScene), width=20, height=3)
        login.place(relx=.35, rely=.25, relwidth=.3, relh=.2)

        register = tk.Button(frame, text="Register", font=tkFont.Font(size=20),
                             command=lambda: self.master.switchScene(registerScene))
        register.place(relx=.35, rely=.5, relwidth=.3, relh=.2)

        self.master.createBackButton(frame, startScene)


# Login Page, Need to work on Login Function
class loginScene(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Frame to hold widgets
        frame = tk.Frame(root, bg=bgColor)
        frame.place(relwidth=1, relheight=1)

        # Message at the Top
        header = tk.Message(frame, text="Login", bg=bgColor, fg=fgColor, font=tkFont.Font(size=30), width=400)
        header.pack(side="top")
        message = tk.Label(frame, text="Login using a valid username and password", bg=bgColor, fg=fgColor,
                           font=tkFont.Font(size=12))
        message.pack(side="top")

        # Username
        userBox = tk.LabelFrame(frame, bg=bgColor, text="Username", fg=fgColor)
        userBox.place(relx=.1, rely=.3, relw=.8, relh=.12)
        userEntry = tk.Entry(userBox)
        userEntry.place(relx=.025, rely=.1, relw=.95, relh=.7)

        # Password
        passBox = tk.LabelFrame(frame, bg=bgColor, text="Password", fg=fgColor)
        passBox.place(relx=.1, rely=.5, relw=.8, relh=.12)
        passEntry = tk.Entry(passBox, show="*")
        passEntry.place(relx=.025, rely=.1, relw=.95, relh=.7)

        # Button
        confirm = tk.Button(frame, text="Login", command=lambda: self.login(userEntry.get(), passEntry.get()))
        confirm.place(relx=.35, rely=.85, relw=.3, relh=.1)
        self.master.createBackButton(frame, checkScene)


    def login(self, username, password):

        # Query the table for the username and password
        sql = "SELECT iduser, password FROM user WHERE username = %(username)s"
        val = {'username': username}

        mycursor.execute(sql, val)
        login = mycursor.fetchall()

        # If the results is not empty then we have a good login, and we need to set the currUser variable

        if len(login) != 0 and login[0][1] == password:
            changeUser(login[0][0])
            self.master.switchScene(homeScene)
        else: # Bad Login
            print("Error: Username or Password is incorrect")


# Register Page, Need work on Register Function
class registerScene(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Container
        frame = tk.Frame(root, bg=bgColor)
        frame.place(relwidth=1, relheight=1)

        # Top Message
        header = tk.Message(frame, text="Register", bg=bgColor, fg=fgColor, font=tkFont.Font(size=30), width=400)
        header.pack(side="top")

        # Below Top Message
        self.message = tk.Label(frame, text="", bg=bgColor, fg=fgColor, font=tkFont.Font(size=12))
        self.message.pack(side="top")

        # Username box
        userBox = tk.LabelFrame(frame, bg=bgColor, text="Username", fg=fgColor)
        userBox.place(relx=.1, rely=.2, relw=.8, relh=.1)
        userEntry = tk.Entry(userBox)
        userEntry.place(relx=.025, rely=.1, relw=.95, relh=.7)

        # Password box
        passBox = tk.LabelFrame(frame, bg=bgColor, text="Password", fg=fgColor)
        passBox.place(relx=.1, rely=.32, relw=.8, relh=.1)
        passEntry = tk.Entry(passBox, show="*")
        passEntry.place(relx=.025, rely=.1, relw=.95, relh=.7)

        # Confirm Password Box
        confirmPassBox = tk.LabelFrame(frame, bg=bgColor, text="Confirm Password", fg=fgColor)
        confirmPassBox.place(relx=.1, rely=.44, relw=.8, relh=.1)
        confirmPassEntry = tk.Entry(confirmPassBox, show="*")
        confirmPassEntry.place(relx=.025, rely=.1, relw=.95, relh=.7)

        # Email Box
        emailBox = tk.LabelFrame(frame, bg=bgColor, text="Email", fg=fgColor)
        emailBox.place(relx=.1, rely=.56, relw=.8, relh=.1)
        emailEntry = tk.Entry(emailBox)
        emailEntry.place(relx=.025, rely=.1, relw=.95, relh=.7)

        # Address Box
        addressBox = tk.LabelFrame(frame, bg=bgColor, text="Address", fg=fgColor)
        addressBox.place(relx=.1, rely=.68, relw=.8, relh=.1)
        addressEntry = tk.Entry(addressBox)
        addressEntry.place(relx=.025, rely=.1, relw=.95, relh=.7)

        # Button
        confirm = tk.Button(frame, text="Register", command=lambda: self.register(userEntry.get(), passEntry.get(), confirmPassEntry.get(), emailEntry.get(), addressEntry.get()))
        confirm.place(relx=.5, rely=.85, relw=.3, relh=.065)
        self.master.createBackButton(frame, checkScene)

    # Checks for valid inputs and switches to the next scene.  Needs work
    def register(self, user, password, confPassword, email, address):

        if user != '' and password == confPassword and email != '' and address != '':
            sql = "INSERT INTO user (username, password, email, address) VALUES (%s, %s, %s, %s)"
            val = (user, password, email, address)
            mycursor.execute(sql, val)
            mydb.commit()
            mycursor.execute("SELECT iduser FROM user ORDER BY iduser DESC LIMIT 1")
            result = mycursor.fetchall()

            changeUser(result[0][0])
            self.master.switchScene(primaryScene)
        else:
            self.message.configure(text="That is an invalid set of entries.")


# Selection Scene - Primary
class primaryScene(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        frame = tk.Frame(root, bg=bgColor)
        frame.place(relwidth=1, relheight=1)

        # Human Service
        human = tk.BooleanVar()
        human.set(False)
        box1 = tk.Checkbutton(frame, text="Human", bg=bgColor, fg=fgColor, selectcolor="black", variable=human)
        box1.grid(column=0, row=2, sticky='nsew')

        # Arts and Culture
        arts = tk.BooleanVar()
        arts.set(False)
        box2 = tk.Checkbutton(frame, text="Arts", bg=bgColor, fg=fgColor, selectcolor="black", variable=arts)
        box2.grid(column=1, row=2, sticky='nsew')

        # Health
        health = tk.BooleanVar()
        health.set(False)
        box3 = tk.Checkbutton(frame, text="Health", bg=bgColor, fg=fgColor, selectcolor="black", variable=health)
        box3.grid(column=2, row=2, sticky='nsew')

        # Community Development
        community = tk.BooleanVar()
        community.set(False)
        box4 = tk.Checkbutton(frame, text="Community", bg=bgColor, fg=fgColor, selectcolor="black", variable=community)
        box4.grid(column=0, row=3, sticky='nsew')

        # Education
        education = tk.BooleanVar()
        education.set(False)
        box5 = tk.Checkbutton(frame, text="Education", bg=bgColor, fg=fgColor, selectcolor="black", variable=education)
        box5.grid(column=1, row=3, sticky='nsew')

        # International
        international = tk.BooleanVar()
        international.set(False)
        box6 = tk.Checkbutton(frame, text="International", bg=bgColor, fg=fgColor, selectcolor="black", variable=international)
        box6.grid(column=2, row=3, sticky='nsew')

        # Animals
        animal = tk.BooleanVar()
        animal.set(False)
        box7 = tk.Checkbutton(frame, text="Animals", bg=bgColor, fg=fgColor, selectcolor="black", variable=animal)
        box7.grid(column=0, row=4, sticky='nsew')

        # Religion
        religion = tk.BooleanVar()
        religion.set(False)
        box8 = tk.Checkbutton(frame, text="Religion", bg=bgColor, fg=fgColor, selectcolor="black", variable=religion)
        box8.grid(column=1, row=4, sticky='nsew')

        # Environment
        environment = tk.BooleanVar()
        environment.set(False)
        box9 = tk.Checkbutton(frame, text="Environment", bg=bgColor, fg=fgColor, selectcolor="black", variable=environment)
        box9.grid(column=2, row=4, sticky='nsew')

        # Submit
        button = tk.Button(frame, text="Done", font=tkFont.Font(size=12),
                           command=lambda: self.submit(human.get(), arts.get(), health.get(), community.get(), education.get(), international.get(), animal.get(), religion.get(), environment.get()))
        button.grid(column=1, row=5, sticky='nsew')

        # Buffer & Text
        tk.Label(frame, text="", bg=bgColor).grid(column=0, row=0)
        message = tk.Message(frame, text="Select all types of charities that interest you", bg=bgColor, fg=fgColor, font=tkFont.Font(size=20), width=400, justify=tk.CENTER)
        message.grid(column=0, row=1, columnspan=3)
        tk.Label(frame, text="", bg=bgColor).grid(column=0, row=7)

        # Scaling
        frame.columnconfigure(0, weight=3)
        frame.columnconfigure(1, weight=3)
        frame.columnconfigure(2, weight=3)
        frame.rowconfigure(1, weight=3)
        frame.rowconfigure(2, weight=3)
        frame.rowconfigure(3, weight=3)
        frame.rowconfigure(4, weight=3)

    def submit(self, human, arts, health, community, education, international, animal, religion, environment):
        # switch to next scene with self.master.switchScene(sceondaryScene)
        sql = "UPDATE user SET HumSer = %(human)s, ArtsCraft = %(arts)s, Hea = %(health)s, ComDev = %(community)s, Edu = %(education)s, Inter = %(international)s, Ani = %(animal)s, Rel = %(religion)s, Env = %(environment)s WHERE iduser = %(currUser)s"

        val = { 'human': int(human), 'arts': int(arts), 'health': int(health), 'community': int(community), 'education': int(education), 'international': int(international), 'animal': int(animal), 'religion': int(religion), 'environment': int(environment), 'currUser': currUser}

        mycursor.execute(sql, val)
        mydb.commit()
        self.master.switchScene(secondaryScene)


# Selection Scene - Secondary
class secondaryScene(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Creates container for widgets
        frame = tk.Frame(root, bg=bgColor)
        frame.place(relwidth=1, relheight=1)

        # Buffer & Text
        tk.Label(frame, text="", bg=bgColor).pack(side="top")
        message = tk.Message(frame, text="What factors are important when donating?", bg=bgColor, fg=fgColor,
                             font=tkFont.Font(size=20), width=400, justify=tk.CENTER)
        message.pack(side="top")
        tk.Label(frame, text="", bg=bgColor).pack(side="top")

        secondaryLabels = ["Small Charities",
                           "High Transparency Charities",
                           "Low Financial Health Charities",
                           "High Rated Charities",
                           "Highly Expense Charities"]

        # Creates a listbox of secondary labels
        list = tk.Listbox(frame, font=tkFont.Font(size=12), selectmode=tk.MULTIPLE, width=30, justify=tk.CENTER)
        for label in secondaryLabels:
            list.insert(tk.END, label)
        list.pack(side="top")

        # Submit
        tk.Label(frame, text="", bg=bgColor).pack(side="top")
        button = tk.Button(frame, text="Done", font=tkFont.Font(size=12), command=lambda: self.submit(list))
        button.pack(side="top")
        self.master.createBackButton(frame, primaryScene)

    def submit(self, list):
        list = list.curselection()
        values = []
        sql = "UPDATE user SET Small = %(small)s, HighTrans = %(trans)s, LowFin = %(fin)s, HighRat = %(rat)s, HighExp = %(exp)s WHERE iduser = %(currUser)s"
        for x in range(0, 5):
            if x in list:
                values.append(1)
            else:
                values.append(0)
        values.append(currUser)
        selected = {'small': values[0], 'trans': values[1], 'fin': values[2], 'rat': values[3], 'exp': values[4], 'currUser': values[5]}
        mycursor.execute(sql, selected)

        self.master.switchScene(resultScene)


# Results of query
class resultScene(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Creates frame for widgets
        frame = tk.Frame(root, bg=bgColor)
        frame.place(relwidth=1, relheight=1)

        # Create buffering
        tk.Label(frame, text="", bg=bgColor, font=tkFont.Font(size=6)).pack(side="top")
        tk.Label(frame, text="", bg=bgColor, font=tkFont.Font(size=6)).pack(side="bottom")

        # Query for user's settings

        sql = "SELECT HumSer, ArtsCraft, Hea, ComDev, Edu, Inter, Ani, Rel, Env, Small, HighTrans, LowFin, HighRat, HighExp FROM user WHERE iduser = " + str(currUser)
        val = ()

        mycursor.execute(sql)
        settings = mycursor.fetchall()
        result = []
        whereClause = ""
        if 1 in settings[0]:
            whereClause += "WHERE"
            numberOfCat = 0
            numberOfFactors = 0
            hadCat = False

        for x in range(9, 14): # Count how many factors we have
            if settings[0][x]:
                numberOfFactors += 1

        for x in range(0, 9):  # counts how many categories we have
            if settings[0][x]:
                numberOfCat += 1

        if 1 in settings[0][:9]: # We have 1 or more categories selected
            hadCat = True
            whereClause += " category IN ("

            for x in range(0, 14):
                if (x == 0 and settings[0][x] == 1):
                    whereClause += "'Human Services'"
                    numberOfCat -= 1
                    if numberOfCat != 0:
                        whereClause += ","

                elif (x == 1 and settings[0][x] == 1):
                    whereClause += " 'Arts, Culture, Humanities'"
                    numberOfCat -= 1
                    if numberOfCat != 0:
                        whereClause += ","

                elif (x == 2 and settings[0][x] == 1):
                    whereClause += " 'Health' "
                    numberOfCat -= 1
                    if numberOfCat != 0:
                        whereClause += ","

                elif (x == 3 and settings[0][x] == 1):
                    whereClause += " 'Community Development'"
                    numberOfCat -= 1
                    if numberOfCat != 0:
                        whereClause += ","

                elif (x == 4 and settings[0][x] == 1):
                    whereClause += " 'Education'"
                    numberOfCat -= 1
                    if numberOfCat != 0:
                        whereClause += ","

                elif (x == 5 and settings[0][x] == 1):
                    whereClause += " 'Internatinal'"
                    numberOfCat -= 1
                    if numberOfCat != 0:
                        whereClause += ","

                elif (x == 6 and settings[0][x] == 1):
                    whereClause += " 'Animals'"
                    numberOfCat -= 1
                    if numberOfCat != 0:
                        whereClause += ","

                elif (x == 7 and settings[0][x] == 1):
                    whereClause += " 'Religion'"
                    numberOfCat -= 1
                    if numberOfCat != 0:
                        whereClause += ","

                elif (x == 8 and settings[0][x] == 1):
                    whereClause += " 'Environment'"
                    numberOfCat -= 1
                    if numberOfCat != 0:
                        whereClause += ","


            whereClause += ")"

            if numberOfFactors > 0:
                whereClause += ' AND '

        for x in range(9,14):
            if (x == 9 and settings[0][x] == 1):  # Small Size
                whereClause += " size = 'small'"
                numberOfFactors -= 1
                if numberOfFactors != 0:
                    whereClause += " AND "

            elif (x == 10 and settings[0][x] == 1):  # ascore
                whereClause += " ascore > 50 "
                numberOfFactors -= 1
                if numberOfFactors != 0:
                    whereClause += " AND "

            elif (x == 11 and settings[0][x] == 1):  # fscore
                whereClause += " fscore < 50 "
                numberOfFactors -= 1
                if numberOfFactors != 0:
                    whereClause += " AND "

            elif (x == 12 and settings[0][x] == 1):  # score
                whereClause += " score > 50 "
                numberOfFactors -= 1
                if numberOfFactors != 0:
                    whereClause += " AND "

            elif (x == 13 and settings[0][x] == 1):  # tot_exp
                whereClause += " tot_exp > 50 "

        sql = "SELECT name, motto, description, score, category, subcategory, Website, Facebook, Twitter, Address, city, state FROM charnavandusachar " + whereClause


        mycursor.execute(sql)
        result = mycursor.fetchall()

        # Creates Listbox of results/charities
        charityList = tk.Listbox(frame, width=60, font=tkFont.Font(size=12), justify=tk.LEFT)
        for row in result:
            charityList.insert(tk.END, row[0])

        charityList.place(relx=.1, rely=.2, relw=.7, relh=.6)

        # Creates scroll bar
        scrollBar = tk.Scrollbar(charityList)
        charityList.config(yscrollcommand=scrollBar.set)
        scrollBar.pack(side="right", fill="y")
        scrollBar.config(command=charityList.yview)

        # Title
        tk.Message(frame, text="My Matches", bg=bgColor, width=200, font=tkFont.Font(size=16)).pack(side="top")

        # Details Button
        details = tk.Button(frame, text="Details", font=tkFont.Font(size=16), command=lambda: self.master.displayDetails(result[charityList.curselection()[0]]))
        details.place(relx=.825, rely=.45, relw=.15, relh=.1)
        self.master.createBackButton(frame, homeScene)


# Account Page
class accountScene(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Creates container for widgets
        frame = tk.Frame(root, bg=bgColor)
        frame.place(relwidth=1, relheight=1)

        sql = "SELECT username, email, address FROM user WHERE iduser = %(userid)s"
        val = {'userid': currUser}

        mycursor.execute(sql, val)
        info = mycursor.fetchall()

        tk.Label(frame, text="", bg=bgColor).pack(side="top")
        tk.Message(frame, text="My Account", bg=bgColor, fg=fgColor, width=900, font=tkFont.Font(size=20)).pack(side="top")
        tk.Message(frame, text="Name: " + info[0][0], bg=bgColor, fg=fgColor, width=900, font=tkFont.Font(size=12), justify=tk.LEFT).pack(side="top")
        tk.Message(frame, text="Email: " + info[0][1], bg=bgColor, fg=fgColor, width=900, font=tkFont.Font(size=12), justify=tk.LEFT).pack(side="top")
        tk.Message(frame, text="Address: " + info[0][2], bg=bgColor, fg=fgColor, width=900, font=tkFont.Font(size=12), justify=tk.LEFT).pack(side="top")
        tk.Message(frame, text="My Charities: ", bg=bgColor, fg=fgColor, width=900, font=tkFont.Font(size=12), justify=tk.LEFT).place(relx=.4, rely=.45)
        self.master.createBackButton(frame, homeScene)
        charityList = tk.Listbox(frame, width=60, selectmode=tk.SINGLE, font=tkFont.Font(size=12), justify=tk.LEFT)
        charityList.place(relx=.1, rely=.5, relw=.8, relh=.3)
        #details = tk.Button(frame, text="Details", )


app = Application(master=root)
app.master.title("Charity Matchmaker - hackeroos")

app.mainloop()