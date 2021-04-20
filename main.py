import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
from urllib.request import Request, urlopen
from io import BytesIO
import mysql.connector

bgColor = "#990000"
fgColor = "white"
root = tk.Tk()

def changeUser(user):
    global currUser
    currUser = user

mydb = mysql.connector.connect(host="localhost", username="root", password="", database="hackathon")

mycursor = mydb.cursor()

print(mydb)

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()

        # Create canvas
        canvas = tk.Canvas(root, height=480, width=640)
        canvas.pack()

        self.currFrame = None
        self.switchScene(startScene) #startScene

    def switchScene(self, newFrame):
        if self.currFrame is not None:
            self.currFrame.pack_forget()
            self.currFrame.destroy()

        self.currFrame = newFrame(self)
        self.currFrame.pack()

    def displayDetails(self, charity):
        newWindow = tk.Toplevel(bg=bgColor)
        tk.Label(newWindow, text=charity.name, font=tkFont.Font(size=12), bg=bgColor, fg=fgColor).pack(side="top")
        try:
            self.displayPicture(charity, newWindow)
        except:
            pass

    def displayPicture(self, charity, newWindow):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        req = Request(charity.pic, headers=headers)
        picture = urlopen(req).read()
        im = Image.open(BytesIO(picture))

        im = im.resize((200, 200), Image.ANTIALIAS)

        canvas = tk.Canvas(newWindow, width=200, height=200)
        canvas.pack()

        canvas.image = ImageTk.PhotoImage(im)
        canvas.create_image(100, 100, image=canvas.image, anchor=tk.CENTER)


# Home Scene - Nothing atm
class homeScene(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        frame = tk.Frame(root, bg=bgColor)
        frame.place(relwidth=.8, relheight=1)

        sideBar = tk.Canvas(root, bg="#660000")
        sideBar.place(relh=1, relw=.2)

        home = tk.Button(sideBar, text="Home", command=lambda: self.switchScene(homeScene))
        home.place(relx=.1, rely=0.125, relw=.8, relh=.1)


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

        login = tk.Button(frame, text="Login", font=tkFont.Font(size=20),
                          command=lambda: self.master.switchScene(loginScene), width=20, height=3)
        login.place(relx=.35, rely=.25, relwidth=.3, relh=.2)

        register = tk.Button(frame, text="Register", font=tkFont.Font(size=20),
                             command=lambda: self.master.switchScene(registerScene))
        register.place(relx=.35, rely=.5, relwidth=.3, relh=.2)


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
        passEntry = tk.Entry(passBox)
        passEntry.place(relx=.025, rely=.1, relw=.95, relh=.7)

        # Button
        confirm = tk.Button(frame, text="Login", command=lambda: self.login(userEntry.get(), passEntry.get()))
        confirm.place(relx=.5, rely=.85, relw=.3, relh=.065)

    # Needs Work
    def login(self, username, password):

        # Query the table for the username and password
        sql = "SELECT iduser, password FROM user WHERE username = %(username)s"
        val = {'username': username}

        mycursor.execute(sql, val)
        login = mycursor.fetchall()

        # If the results is not empty then we have a good login, and we need to set the currUser variable
        # Else
        if len(login) != 0 and login[0][1] == password:
            currUser = login[0][0]
            self.master.switchScene(homeScene)

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
        passEntry = tk.Entry(passBox)
        passEntry.place(relx=.025, rely=.1, relw=.95, relh=.7)

        # Confirm Password Box
        confirmPassBox = tk.LabelFrame(frame, bg=bgColor, text="Confirm Password", fg=fgColor)
        confirmPassBox.place(relx=.1, rely=.44, relw=.8, relh=.1)
        confirmPassEntry = tk.Entry(confirmPassBox)
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
            print(result[0][0])
            print(currUser)
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
        print(currUser)
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

    def submit(self, list):
        list = list.curselection()
        values = []
        print(type(list))
        sql = "UPDATE user SET Small = %(small)s, HighTrans = %(trans)s, LowFin = %(fin)s, HighRat = %(rat)s, HighExp = %(exp)s WHERE iduser = %(currUser)s"
        for x in range(0, 5):
            if x in list:
                values.append(1)
            else:
                values.append(0)
        values.append(currUser)
        print(values)
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
        tk.Label(frame, text="", bg=bgColor, font=tkFont.Font(size=20)).pack(side="top")
        tk.Label(frame, text="", bg=bgColor, font=tkFont.Font(size=20)).pack(side="bottom")

        # Creates Listbox of results/charities
        results = tk.Listbox(frame, font=tkFont.Font(size=12), width=60, selectmode=tk.SINGLE, justify=tk.LEFT)

        # Query for valid charities
        charities = ["a", "b", "c", "d"]

        # Populates results
        for x in charities:
            results.insert(tk.END, charities)

        results.pack(side="top")

        # Creates scroll bar
        scrollBar = tk.Scrollbar(results)
        scrollBar.pack(side="right", fill="y")
        scrollBar.config(command=results.yview)

        details = tk.Button(frame, text="Details", font=tkFont.Font(size=20), command=lambda: self.displayDetails(results.curselection()[0]))
        details.pack(side="bottom")


class account(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Creates container for widgets
        frame = tk.Frame(root, bg=bgColor)
        frame.place(relwidth=1, relheight=1)

        "SELECT username, passowrd, email, address WHERE iduser=%d"

        tk.Label(frame, text="", bg=bgColor).pack(side="top")
        message = tk.Message(frame, text="", bg=bgColor, font=tkFont.Font(size=12))

app = Application(master=root)
app.master.title("Charity Matchmaker")

app.mainloop()