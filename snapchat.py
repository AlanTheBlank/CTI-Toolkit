from os import mkdir, remove, rmdir, listdir
from tkinter import Tk, Toplevel, ttk, Label, Entry, Button
from tkinter.filedialog import asksaveasfilename
from subprocess import run, call
from os import startfile, getcwd
from geopy.geocoders import Nominatim
from typing import Union

class Snapchat:

    def __init__(self, parent: Union[Tk, Toplevel], long: str = None, lat: str = None, city: str = None):
        self.parent = parent
        self.long = long
        self.lat = lat
        self.city = city
        self.parent.iconify()
        try:
            mkdir("temp")
        except FileExistsError:
            print("Folder already exists, possible messy exit previously")
        self.snapwindow = self.genWindow()
        self.genWidgets()

    # Generates the window
    def genWindow(self) -> Toplevel:
        snapwindow = Toplevel(self.parent)
        snapwindow.title("Snapchat")
        snapwindow.resizable(False, False)
        snapwindow.geometry("+%d+%d" % (self.parent.winfo_x(), self.parent.winfo_y()))
        snapwindow.protocol("WM_DELETE_WINDOW", lambda: self.closewin())
        return snapwindow

    # Generates the widgets to be displayed on the window
    def genWidgets(self) -> None:
        # Labels
        latLabel = Label(self.snapwindow, text="Latitude: ")
        longLabel = Label(self.snapwindow, text="Longitude: ")
        cityLabel = Label(self.snapwindow, text="City: ")
        radiusLabel = Label(self.snapwindow, text="Radius (meters): ")

        # Entries
        latEntry = Entry(self.snapwindow, width=20)
        longEntry = Entry(self.snapwindow, width=20)
        cityEntry = Entry(self.snapwindow, width=20)
        radiusEntry = Entry(self.snapwindow, width=10)

        radiusEntry.insert(0, "10000")

        # Button
        SearchButton = Button(self.snapwindow, text="Search", command=lambda: self.verifyInput(latEntry.get(), longEntry.get(), cityEntry.get(), radiusEntry.get()))
        SaveButton = Button(self.snapwindow, text="Save", command=lambda: self.saveFile())

        # Autofill
        if self.long:
            longEntry.insert(0, self.long)
        if self.lat:
            latEntry.insert(0, self.lat)
        if self.city:
            cityEntry.insert(0, self.city)

        # Treeview
        self.details = ttk.Treeview(self.snapwindow, show="headings", height="6")

        self.details['columns'] = ("Name", "Type")
        self.details.column("#0", width=0)
        self.details.column("Name", width=350)
        self.details.column("Type", width=150, minwidth=80)

        self.details.heading("#0", text="")
        self.details.heading("Name", text="Name")
        self.details.heading("Type", text="Type")

        scroll = ttk.Scrollbar(self.snapwindow, orient="vertical", command=self.details.yview)
        self.details.config(yscrollcommand=scroll.set)
        self.details.bind("<Double-1>", self.openFile)

        # Grid Layout
        latLabel.grid(row=0, column=0, sticky="E")
        latEntry.grid(row=0, column=1, padx=(0, 5))
        longLabel.grid(row=0, column=2, sticky="E")
        longEntry.grid(row=0, column=3, padx=(0, 5))
        radiusLabel.grid(row=1, column=2, sticky="E")
        radiusEntry.grid(row=1, column=3, padx=(0, 5))
        cityLabel.grid(row=1, column=0, sticky="E")
        cityEntry.grid(row=1, column=1, padx=(0, 5))

        SearchButton.grid(row=2, column=2, columnspan=1, sticky="NSEW", pady=10)
        SaveButton.grid(row=4, column=2, pady=(0, 10))

        self.details.grid(row=3, column=0, columnspan=4, padx=(5, 0), pady=5)
        scroll.grid(row=3, column=4, padx=(0, 5), sticky="NS")

    # Opens the images displayed in the treeview when double clicked
    def openFile(self, event) -> None:
        filename = getcwd() + "/temp/" + self.details.item(self.details.focus())['values'][0]
        try:
            startfile(filename)
        except AttributeError:
            call(['open', filename])

    # Saves the file to a directory of their choice from the temp folder
    def saveFile(self) -> None:
        if self.details.item(self.details.focus())['values'][1] == "Image":
            file = asksaveasfilename(initialfile=self.details.item(self.details.focus())['values'][0].rsplit(".", 1)[0], filetypes=[("JPG image", "*.jpg")]) + ".jpg"
        else:
            file = asksaveasfilename(initialfile=self.details.item(self.details.focus())['values'][0].rsplit(".", 1)[0], filetypes=[("MPEG video", "*.mp4")]) + ".mp4"
        if len(file) > 4:
            with open(file, "wb+") as f:
                with open(getcwd() + "/temp/" + self.details.item(self.details.focus())['values'][0], "rb") as f2:
                    f.write(f2.read())

    # Checks to see if the range is an int, and gets the lat, long of the city if chosen
    def verifyInput(self, lat: str, long: str, city: str, range: str) -> None:
        try:
            rangeInt = int(range)
        except ValueError:
            print("Error, radius isn't a number. Resorting to default!")
            rangeInt = 10000
        if lat == "":
            geo = Nominatim(user_agent="CTI Toolkit")
            location = geo.geocode(city)
            lat = location.latitude
            long = location.longitude

        coords: str = str(lat) + "," + str(long)

        self.searchSnap(coords, rangeInt)

    # Clears the temp folder, and then runs the snapmap_archiver python module
    def searchSnap(self, coords: str, range: int) -> None:
        # Cleanup
        self.details.delete(*self.details.get_children())
        for files in listdir("temp"):
            remove("temp/" + files)

        # Runs the command (Will freeze the program)
        run('python -m snapmap_archiver -o temp -l=\"{}\" -r {}'.format(coords, range))

        # Lists the output
        for files in listdir("temp"):
            if "mp4" in files.rsplit(".")[1]:
                self.details.insert("", 'end', values=(files, "Video"))
            else:
                self.details.insert("", 'end', values=(files, "Image"))

    # Closes the window
    def closewin(self) -> None:
        for file in listdir("temp"):
            remove("temp/" + file)
        rmdir("temp")
        self.parent.deiconify()
        self.snapwindow.destroy()
