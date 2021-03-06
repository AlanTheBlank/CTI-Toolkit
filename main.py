from tkinter import Tk, Label, Button
import web
import API
import snapchat

class Main:
    def __init__(self, root: Tk) -> None:
        self.root = root
        self.configWindow()
        self.genWidgets()

    # Generates the buttons displayed on the main window
    def genWidgets(self) -> None:
        Web = Button(self.root, text="Web", command=lambda: self.OpenWeb())
        Snapchat = Button(self.root, text="Snapchat", command=lambda: self.OpenSnap())
        API = Button(self.root, text="API Settings", command=lambda: self.OpenAPI())
        Quit = Button(self.root, text="Exit", command=lambda: self.root.destroy())
    
        Web.grid(row=1, column=1, sticky="NSEW", pady=(0, 10))
        Snapchat.grid(row=2, column=1, sticky="NSEW", pady=(0, 10))
        API.grid(row=3, column=1, sticky="NSEW", pady=(0, 10))
        Quit.grid(row=4, column=1, sticky="NSEW", pady=(0, 10))

        # Generates the title
        title = Label(self.root, text="CTI Toolkit", font="none 24 bold")
        title.grid(row=0, column=0, columnspan=3, padx=(40, 40), pady=(0, 10))

    # Configures the window
    def configWindow(self) -> None:
        self.root.title("CTI Toolkit - AlanTheBlank")
        self.root.resizable(False, False)
        self.root.eval('tk::PlaceWindow . center')

    # Opens the web frame
    def OpenWeb(self) -> None:
        web.Web(self.root)

    # Opens the snap frame
    def OpenSnap(self) -> None:
        snapchat.Snapchat(self.root)

    # Opens the API frame
    def OpenAPI(self) -> None:
        API.API(self.root)


if __name__ == "__main__":
    root = Tk()
    Main(root)
    root.mainloop()
