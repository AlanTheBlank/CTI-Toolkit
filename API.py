from tkinter import Tk, Toplevel, Label, Entry, Button, TclError
import json
from typing import Union

class API:
    ipInfoVisible = False
    vtKeyVisible = False

    def __init__(self, root: Tk) -> None:
        self.root = root
        root.withdraw()
        self.apiwindow = self.genWindow()
        self.genWidgets()

    # Generates the window
    def genWindow(self) -> Toplevel:
        apiwindow = Toplevel(self.root)
        apiwindow.resizable(False, False)
        apiwindow.title("API")
        apiwindow.geometry("+%d+%d" % (self.root.winfo_x(), self.root.winfo_y()))
        apiwindow.protocol("WM_DELETE_WINDOW", lambda: self.closewin())
        return apiwindow

    # Handles the closing of the windows.  Opens previously open window
    def closewin(self) -> None:
        self.root.deiconify()
        self.apiwindow.destroy()

    # Toggles the visibility of the API keys
    def visibility(self, entry: Entry, apientry: int) -> None:
        if apientry == 0:
            if self.ipInfoVisible:
                entry.config(show="\u2022")
                self.ipInfoVisible = False
            else:
                entry.config(show="")
                self.ipInfoVisible = True
        elif apientry == 1:
            if self.vtKeyVisible:
                entry.config(show="\u2022")
                self.vtKeyVisible = False
            else:
                entry.config(show="")
                self.vtKeyVisible = True
        else:
            print("Unknown apientry value")

    # Saves the API keys to api.json
    def SaveAPI(self, entries: list[Entry]) -> None:
        APIKeys = {
            "ipinfo": entries[0].get(),
            "shodan": entries[1].get()
        }
        json.dump(APIKeys, open("api.json", "w+"))
        self.closewin()

    # Get the API keys currently saved in api.json
    def getKeys(self) -> Union[dict, None]:
        try:
            return json.load(open("api.json", "r+"))
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    # Generates the widgets for the window
    def genWidgets(self) -> None:
        entries: list[Entry] = []
        currentKeys = self.getKeys()
        # Labels
        ipInfoLabel = Label(self.apiwindow, text="ipInfo: ")
        ShodanKeyLabel = Label(self.apiwindow, text="Shodan: ")

        # Entry Fields
        ipInfoEntry = Entry(self.apiwindow, width=15, show="\u2022")
        ShodanKeyEntry = Entry(self.apiwindow, width=15, show="\u2022")
        
        # Load already saved keys
        try:
            ipInfoEntry.insert(0, currentKeys["ipinfo"])
        except (KeyError, TclError, TypeError):
            ipInfoEntry.insert(0, "")
        try:
            ShodanKeyEntry.insert(0, currentKeys['shodan'])
        except (KeyError, TclError, TypeError):
            ShodanKeyEntry.insert(0, "")


        entries.append(ipInfoEntry)
        entries.append(ShodanKeyEntry)
    
        # Visiblity buttons
        ipInfoButton = Button(self.apiwindow, text="show", command=lambda: self.visibility(ipInfoEntry, 0))
        ShodanKeyButton = Button(self.apiwindow, text="show", command=lambda: self.visibility(ShodanKeyEntry, 0))

        # General button
        submit = Button(self.apiwindow, text="Save", command=lambda: self.SaveAPI(entries))

        # Grid
        ipInfoLabel.grid(row=0, column=0, padx=(10, 0), pady=(10, 10), sticky="E")
        ipInfoEntry.grid(row=0, column=1, pady=(10, 10))
        ipInfoButton.grid(row=0, column=2, padx=(5, 10), pady=(10, 10))
        ShodanKeyLabel.grid(row=1, column=0, padx=(10, 0), pady=(0, 10), sticky="E")
        ShodanKeyEntry.grid(row=1, column=1)
        ShodanKeyButton.grid(row=1, column=2, padx=(5, 10))
        submit.grid(row=2, column=1, pady=(0, 10))
