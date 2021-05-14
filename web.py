from tkinter import Tk, Button, Toplevel, Label, Entry, LabelFrame, messagebox, END
import ipinfo
import json
import snapchat
from shodan import Shodan, exception
import webbrowser
from requests import HTTPError

class Web:

    def __init__(self, root: Tk) -> None:
        self.root = root
        root.withdraw()
        try:
            self.ipinfoAPI = json.load(open("api.json", "r+"))["ipinfo"]
        except (json.JSONDecodeError, FileNotFoundError):
            self.ipinfoAPI = None
        try:
            self.shodanAPI = json.load(open("api.json", "r+"))["shodan"]
        except (json.JSONDecodeError, FileNotFoundError):
            self.shodanAPI = None
        self.webwindow = self.genWindow()
        self.genFrames()
        self.genWidgets()

    # Generates the frames which will separate the two APIs being used
    def genFrames(self) -> None:
        self.IPFrame = LabelFrame(self.webwindow, text="IP", padx=5, pady=5)
        self.ShodanFrame = LabelFrame(self.webwindow, text="Shodan", padx=5, pady=5)

        self.IPFrame.grid(row=0, column=0, padx=10, pady=10)
        self.ShodanFrame.grid(row=1, column=0, padx=10, pady=10)

    # Generates the widgets for the two frames
    def genWidgets(self) -> None:
        DetailFields: list[Entry] = []
        DetailShodanFields: list[Entry] = []
        # IP Section
        # Labels
        IPLabel = Label(self.IPFrame, text="IP: ")
        HostnameLabel = Label(self.IPFrame, text="Hostname: ")
        CityLabel = Label(self.IPFrame, text="City: ")
        RegionLabel = Label(self.IPFrame, text="Region: ")
        CountryLabel = Label(self.IPFrame, text="Country: ")
        GPSLabel = Label(self.IPFrame, text="Long/Lat: ")
        OrgLabel = Label(self.IPFrame, text="Org: ")
        TimeLabel = Label(self.IPFrame, text="Timezone: ")

        # Entry fields
        IPEntry = Entry(self.IPFrame, width=20)
        HostnameEntry = Entry(self.IPFrame, width=60, state="disabled")
        CityEntry = Entry(self.IPFrame, width=60, state="disabled")
        RegionEntry = Entry(self.IPFrame, width=60, state="disabled")
        CountryEntry = Entry(self.IPFrame, width=60, state="disabled")
        GPSEntry = Entry(self.IPFrame, width=60, state="disabled")
        OrgEntry = Entry(self.IPFrame, width=60, state="disabled")
        TimeEntry = Entry(self.IPFrame, width=60, state="disabled")

        # Add entries to list
        DetailFields.append(IPEntry)
        DetailFields.append(HostnameEntry)
        DetailFields.append(CityEntry)
        DetailFields.append(RegionEntry)
        DetailFields.append(CountryEntry)
        DetailFields.append(GPSEntry)
        DetailFields.append(OrgEntry)
        DetailFields.append(TimeEntry)

        # Buttons

        # Normal Buttons
        self.SaveButton = Button(self.IPFrame, text="Save", state='disabled', command=lambda: self.saveDetails())
        self.SnapcoordButton = Button(self.IPFrame, text="Snap", state='disabled', command=lambda: snapchat.Snapchat(self.webwindow, lat=GPSEntry.get().split(",")[0], long=GPSEntry.get().split(",")[1]))
        self.SnapcityButton = Button(self.IPFrame, text="Snap", state='disabled', command=lambda: snapchat.Snapchat(self.webwindow, city=CityEntry.get()))

        # Grid layouts
        IPLabel.grid(row=0, column=0, padx=(5, 0))
        IPEntry.grid(row=0, column=1, padx=(0, 5), sticky="W")
        HostnameLabel.grid(row=1, column=0, sticky="E")
        HostnameEntry.grid(row=1, column=1)
        CityLabel.grid(row=1, column=3, sticky="E")
        CityEntry.grid(row=1, column=4)
        self.SnapcityButton.grid(row=1, column=5)
        RegionLabel.grid(row=2, column=0, sticky="E")
        RegionEntry.grid(row=2, column=1)
        CountryLabel.grid(row=2, column=3, sticky="E")
        CountryEntry.grid(row=2, column=4)
        GPSLabel.grid(row=3, column=0, sticky="E")
        GPSEntry.grid(row=3, column=1)
        self.SnapcoordButton.grid(row=3, column=2)
        OrgLabel.grid(row=3, column=3, sticky="E")
        OrgEntry.grid(row=3, column=4)
        TimeLabel.grid(row=4, column=0, sticky="E")
        TimeEntry.grid(row=4, column=1)
        self.SaveButton.grid(row=4, column=3)

        # Shodan
        IPLabelShodan = Label(self.ShodanFrame, text="IP: ")
        CityLabelShodan = Label(self.ShodanFrame, text="City: ")
        CountryLabelShodan = Label(self.ShodanFrame, text="Country: ")
        ASNLabelShodan = Label(self.ShodanFrame, text="ASN: ")
        ISPLabelShodan = Label(self.ShodanFrame, text="ISP: ")
        GPSLabelShodan = Label(self.ShodanFrame, text="Co-ords: ")
        PortsLabelShodan = Label(self.ShodanFrame, text="Ports: ")
        DomainsLabelShodan = Label(self.ShodanFrame, text="Domains: ")
        HostnameLabelShodan = Label(self.ShodanFrame, text="Hostname: ")
        LastUpdatedLabelShodan = Label(self.ShodanFrame, text="Last Updated: ")

        IPEntryShodan = Entry(self.ShodanFrame, width=20)
        CityEntryShodan = Entry(self.ShodanFrame, state='disabled', width=60)
        CountryEntryShodan = Entry(self.ShodanFrame, state='disabled', width=60)
        ASNEntryShodan = Entry(self.ShodanFrame, state='disabled', width=60)
        ISPEntryShodan = Entry(self.ShodanFrame, state='disabled', width=60)
        GPSEntryShodan = Entry(self.ShodanFrame, state='disabled', width=60)
        PortsEntryShodan = Entry(self.ShodanFrame, state='disabled', width=60)
        DomainsEntryShodan = Entry(self.ShodanFrame, state='disabled', width=60)
        HostnameEntryShodan = Entry(self.ShodanFrame, state='disabled', width=60)
        LastUpdatedEntryShodan = Entry(self.ShodanFrame, state='disabled', width=60)

        DetailShodanFields.append(IPEntryShodan)
        DetailShodanFields.append(CityEntryShodan)
        DetailShodanFields.append(CountryEntryShodan)
        DetailShodanFields.append(ASNEntryShodan)
        DetailShodanFields.append(ISPEntryShodan)
        DetailShodanFields.append(GPSEntryShodan)
        DetailShodanFields.append(PortsEntryShodan)
        DetailShodanFields.append(DomainsEntryShodan)
        DetailShodanFields.append(HostnameEntryShodan)
        DetailShodanFields.append(LastUpdatedEntryShodan)

        self.SnapCoordsShodanButton = Button(self.ShodanFrame, text="Snap", state='disabled', command=lambda: snapchat.Snapchat(self.webwindow, lat=GPSEntryShodan.get().split(",")[0], long=GPSEntryShodan.get().split(",")[1]))
        self.SnapCityShodanButton = Button(self.ShodanFrame, text="Snap", state='disabled', command=lambda: snapchat.Snapchat(self.webwindow, city=CityEntryShodan.get()))
        self.OpenShodanButton = Button(self.ShodanFrame, text="Open in browser", state='disabled', command=lambda: webbrowser.open("https://shodan.io/host/{}".format(IPEntryShodan.get()), new=2))

        IPLabelShodan.grid(row=0, column=0, padx=(5, 0), sticky="E")
        IPEntryShodan.grid(row=0, column=1, padx=(0, 5), sticky="W")
        CityLabelShodan.grid(row=1, column=0, sticky="E")
        CityEntryShodan.grid(row=1, column=1)
        self.SnapCityShodanButton.grid(row=1, column=2)
        CountryLabelShodan.grid(row=1, column=3, sticky="E")
        CountryEntryShodan.grid(row=1, column=4)
        ASNLabelShodan.grid(row=2, column=0, sticky="E")
        ASNEntryShodan.grid(row=2, column=1)
        ISPLabelShodan.grid(row=2, column=3, sticky="E")
        ISPEntryShodan.grid(row=2, column=4)
        GPSLabelShodan.grid(row=3, column=0, sticky="E")
        GPSEntryShodan.grid(row=3, column=1)
        self.SnapCoordsShodanButton.grid(row=3, column=2)
        PortsLabelShodan.grid(row=3, column=3, sticky="E")
        PortsEntryShodan.grid(row=3, column=4)
        DomainsLabelShodan.grid(row=4, column=0, sticky="E")
        DomainsEntryShodan.grid(row=4, column=1)
        HostnameLabelShodan.grid(row=4, column=3, sticky="E")
        HostnameEntryShodan.grid(row=4, column=4)
        LastUpdatedLabelShodan.grid(row=5, column=0, sticky="E")
        LastUpdatedEntryShodan.grid(row=5, column=1)
        self.OpenShodanButton.grid(row=5, column=3)

        # Submit Buttons
        if self.IPinfoapivalid():
            IPSubmit = Button(self.IPFrame, text="Submit", command=lambda: self.getDetails(DetailFields, IPEntry.get()))
        else:
            IPSubmit = Button(self.IPFrame, text="Submit", state='disabled')
            messagebox.showerror("Error", "IPInfo is not working.  Is the API key correct?")

        if self.shodanValid():
            IPShodanSubmit = Button(self.ShodanFrame, text="Submit", command=lambda: self.getShodanDetails(DetailShodanFields, IPEntryShodan.get()))
        else:
            messagebox.showerror("Error", "Shodan is not working.  Is the API key correct?")
            IPShodanSubmit = Button(self.ShodanFrame, text="Submit", state='disabled')

        IPSubmit.grid(row=0, column=1, padx=5)
        IPShodanSubmit.grid(row=0, column=1, padx=5)

    # Used to save the ipinfo details that are returned, there are some extra details not displayed.  Saves to the project folder with the IP
    def saveDetails(self) -> None:
        with open(self.data['ip'] + ".json", "w+") as f:
            json.dump(self.data, f)

    # Checks to see if the ipInfo API key is valid, returns a boolean
    def IPinfoapivalid(self) -> bool:
        try:
            ipinfo.getHandler(self.ipinfoAPI).getDetails(None)
            return True
        except HTTPError:
            return False

    # Checks to see if the shodan API key is valid, returns a boolean
    def shodanValid(self) -> bool:
        try:
            test = Shodan(self.shodanAPI)
            test.host('1.1.1.1')
            return True
        except exception.APIError:
            return False

    # Makes the shodan API call and populates the shodan-related entry fields
    def getShodanDetails(self, Details: list[Entry], IP: str) -> None:
        first: bool = True
        for detail in Details:
            detail.config(state='normal')
        self.clearEntries(Details)
        if not IP:
            IP = ipinfo.getHandler(self.ipinfoAPI).getDetails(IP).all['ip']
            print(IP)
        api = Shodan(self.shodanAPI)
        try:
            result = api.host(IP)

            Details[0].delete(0, END)
            Details[0].insert(0, IP)
            Details[1].insert(0, result['city'])
            Details[2].insert(0, result['country_name'])
            Details[3].insert(0, result['asn'])
            Details[4].insert(0, result['isp'])
            Details[5].insert(0, str(result['latitude']) + "," + str(result['longitude']))
            Details[6].insert(0, result['ports'])
            Details[7].insert(0, result['domains'])
            Details[8].insert(0, result['hostnames'])
            Details[9].insert(0, result['last_update'])

            self.SnapCityShodanButton.config(state='normal')
            self.SnapCoordsShodanButton.config(state='normal')
            self.OpenShodanButton.config(state='normal')
        except exception.APIError:

            for detail in Details:
                if first:
                    detail.delete(0, END)
                    detail.insert(0, IP)
                    first = False
                else:
                    detail.delete(0, END)
                    detail.insert(0, "Nothing Found")
        first = True
        for detail in Details:
            if first:
                first = False
            else:
                detail.config(state='disabled')

    # Clears the entry fields for the API being called
    def clearEntries(self, Entries: list[Entry]) -> None:
        for entry in Entries:
            entry.delete(0, END)

    # Makes the ipInfo API call
    def getDetails(self, DetailFields: list[Entry], IP: str) -> None:
        for detail in DetailFields:
            detail.config(state='normal')
        self.clearEntries(DetailFields)

        info = ipinfo.getHandler(self.ipinfoAPI)
        details = info.getDetails(IP)

        self.data = details.all

        for detail in DetailFields:
            detail.config(state='normal')
        
        DetailFields[0].delete(0, END)
        DetailFields[0].insert(0, details.all['ip'])
        DetailFields[1].insert(0, details.all['hostname'])
        DetailFields[2].insert(0, details.all['city'])
        DetailFields[3].insert(0, details.all['region'])
        DetailFields[4].insert(0, details.all['country_name'])
        DetailFields[5].insert(0, details.all['loc'])
        DetailFields[6].insert(0, details.all['org'])
        DetailFields[7].insert(0, details.all['timezone'])

        for detail in DetailFields:
            detail.config(state="disabled")

        DetailFields[0].config(state="normal")
        self.SaveButton.config(state="normal")
        self.SnapcityButton.config(state="normal")
        self.SnapcoordButton.config(state="normal")

    # Generates the window
    def genWindow(self) -> Toplevel:
        webwindow = Toplevel(self.root)
        webwindow.resizable(False, False)
        webwindow.title("Web")
        webwindow.geometry("+%d+%d" % (self.root.winfo_x(), self.root.winfo_y()))
        webwindow.protocol("WM_DELETE_WINDOW", lambda: self.closewin())
        return webwindow

    # Handles the closing of the window, opens the previously open window
    def closewin(self) -> None:
        self.root.deiconify()
        self.webwindow.destroy()
